from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from .models import User


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            print('start')
            serializer = self.get_serializer(data=request.data)
            print(serializer)
            serializer.is_valid(raise_exception=True)
            print('True')
            user = serializer.user
            print(user)
            response = super().post(request, *args, **kwargs)
            print('done')
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
