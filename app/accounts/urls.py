from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, MeView, UserViewSet,
    ChangePasswordUpdateAPIView, UserStatusViewSet
)

urlpatterns = [
    path(
        'auth/login/',
        CustomTokenObtainPairView.as_view(),
        name='user_token_obtain_pair'
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'auth/me/',
        MeView.as_view({"get": "list", "put": "update", "patch": "partial_update"}),
        name="me_data"
    ),
    path(
        'admin/users/',
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="users"
    ),
    path(
        'change-password',
        ChangePasswordUpdateAPIView.as_view(),
        name="user_change_password"
    ),
    path(
        'user-status/',
        UserStatusViewSet.as_view({"get": "list", "post": "create"}),
        name="user-status"
    )
]
