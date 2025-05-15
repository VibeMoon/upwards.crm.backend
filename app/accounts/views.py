from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ViewSet
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from .models import User
from rest_framework.decorators import action


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
        serializer = self.serializer_class(request.user)
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

    @action(detail=False, methods=['patch'])
    def partial_update(self, request):
        """Partial update of user data (PATCH)"""
        serializer = self.serializer_class(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User partially updated successfully",
                "data": serializer.data
            })

        return Response({
            "success": False,
            "message": "Validation error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
