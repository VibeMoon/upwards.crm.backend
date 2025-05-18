from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import exceptions
# from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import User, UserStatus


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    last_online_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    status = UserStatusSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'avatar', 'email', 'first_name',
            'last_name', 'status', 'date_joined',
            'last_online_date', 'groups'
        )


class UserCreateSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    last_online_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = User
        fields = (
            'id', 'avatar', 'email', 'first_name',
            'last_name', 'status', 'password', 'date_joined',
            'last_online_date', 'groups'
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        email = attrs.get('email', '')
        user = User.objects.get(email=email)
        # if user.is_staff:
        #     raise exceptions.AuthenticationFailed(
        #         _('No active account'),
        #         'no_active_account',
        #     )
        return data


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=6)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                "Password fields didn't match."
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                "Old password is not correct"
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
