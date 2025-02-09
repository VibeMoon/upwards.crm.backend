from django.urls import path, include
from .views import SignUpAPIView, SignInAPIView, LogoutAPIView, RoleListCreateView, RoleDetailView, ProfileUpdateView

urlpatterns = [
    path('sign_up/', SignUpAPIView.as_view(), name='sign_up'),
    path('sign_in/', SignInAPIView.as_view(), name='sign_in'),
    path('sign_out/', LogoutAPIView.as_view(), name='sign_out'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('role/', RoleListCreateView.as_view(), name='role_list_create'),
    path('role/<path:id>/', RoleDetailView.as_view(), name='role_detail_delete'),
]