from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth import authenticate, hashers
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import generics, permissions, status, response, exceptions, filters
from rest_framework_simplejwt.tokens import RefreshToken

from asgiref.sync import async_to_sync
from datetime import timezone

from .models import User
from .serializers import *
from .services import GetLoginResponseService
from .permissions import IsChiefOrReadOnly

class SignUpAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = User.objects.create_user(
                                                email=serializer.validated_data["email"],
                                                first_name=serializer.validated_data["first_name"],
                                                last_name=serializer.validated_data["last_name"],
                                                password=serializer.validated_data["password"],
                                                )
                return response.Response(data=GetLoginResponseService.get_login_response(user, request))

            else:
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return response.Response(
                data={"detail": "Пользователь с данной электронной почтой существует!",
                    "status": status.HTTP_409_CONFLICT})

class SignInAPIView(generics.CreateAPIView):
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if not user:
            raise exceptions.AuthenticationFailed

        return response.Response(
            data=GetLoginResponseService.get_login_response(user, request)
        )

class LogoutAPIView(generics.CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = RefreshToken(serializer.validated_data['refresh'])
            token.blacklist()
            return response.Response(data={"detail": "Успешно!", "status": status.HTTP_200_OK})
        except Exception as e:
            return response.Response(data={"error": f"{e}"}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsChiefOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["slug"]
    search_fields = ["title"]
    ordering_fields = ["title"]

    def create(self, request, *args, **kwargs):
        title = request.data.get("title", "").strip()

        slug = request.data.get("slug", "").strip()

        if Role.objects.filter(title__iexact=title).exists():
            return Response({"error": "Роль с таким названием уже существует."}, status=status.HTTP_400_BAD_REQUEST)

        if Role.objects.filter(slug__iexact=slug).exists():
            return Response({"error": "Роль с таким slug уже существует."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)
    
class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        role = self.get_object()
        if role.user_set.exists():
            return Response({"error": "Нельзя удалить роль, которая используется пользователями."}, status=status.HTTP_400_BAD_REQUEST)
        return super().delete(request, *args, **kwargs)