from rest_framework import status, viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.utils.translation import gettext as _
from .serializers import (
    CustomTokenObtainPairSerializer, UserSerializer, ChangePasswordSerializer,
    UserStatusSerializer
)
from .models import User, UserStatus
from config.services import DecodeService


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            response = super().post(request, *args, **kwargs)
            response_data = response.data
            response_data['email'] = user.email

            return Response({
                "success": True,
                "message": "Login successful",
                "data": response_data
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "code": "authentication_error"
            }, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({
                "success": False,
                "message": str(e),
                "code": "authentication_error"
            }, status=status.HTTP_401_UNAUTHORIZED)


class MeView(ViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = self.serializer_class(request.user, context={'request': request})
        return Response({
            "success": True,
            "message": "User data",
            "data": serializer.data
        })

    def update(self, request):
        serializer = self.serializer_class(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User updated successfully",
                "data": serializer.data
            })

        return Response({
            "success": False,
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch', 'put'])
    def partial_update(self, request):
        user = request.user
        data = request.data.copy()

        if 'avatar' in data:
            avatar_data = data.pop('avatar')
            try:
                decoded_file = DecodeService.decode_file(avatar_data)
                user.avatar.save(decoded_file.name, decoded_file, save=True)
            except Exception as e:
                return Response({
                    "success": False,
                    "message": f"Avatar error: {str(e)}",
                }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(
            user,
            data=data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User updated successfully",
                "data": serializer.data
            })

        return Response({
            "success": False,
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserStatusViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return UserStatus.objects.all()

    def get_serializer_class(self):
        return UserStatusSerializer


class UserViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return UserSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ChangePasswordUpdateAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_queryset(self):
        return User.objects.get(id=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": _("Password has been successfully updated"),
                    "status": 200
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
