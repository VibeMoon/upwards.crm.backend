from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
# from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        email = attrs.get('email', '')
        user = User.objects.get(email=email)
        if user.is_staff:
            raise exceptions.AuthenticationFailed(
                _('No active account'),
                'no_active_account',
            )
        return data
