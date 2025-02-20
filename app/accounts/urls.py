from django.urls import path, include
from .views import SignUpAPIView, SignInAPIView, LogoutAPIView, RoleListCreateAPIView, RoleDetailAPIView, ProfileAPIView

urlpatterns = [
    path('sign_up/', SignUpAPIView.as_view(), name='sign_up'),
    path('sign_in/', SignInAPIView.as_view(), name='sign_in'),
    path('sign_out/', LogoutAPIView.as_view(), name='sign_out'),
    path('profile/<int:pk>/', ProfileAPIView.as_view(), name='profile_update'),
    path('role/', RoleListCreateAPIView.as_view(), name='role_list_create'),
    path('role/<path:id>/', RoleDetailAPIView.as_view(), name='role_detail_delete'),
]