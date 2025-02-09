from rest_framework import permissions

from .models import Role

class IsChiefOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated 
        return request.user.is_staff
