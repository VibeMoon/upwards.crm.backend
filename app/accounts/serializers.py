from .models import User, Role, Profile
from rest_framework import serializers

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        ref_name = 'RoleSerializer'

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=False)
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role')
        ref_name = 'UserSerializer'

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")
        ref_name = 'SignUpSerializer'

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Пароль должен быть не менее 8 символов.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну цифру.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну букву.")
        return value

class SignInSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, help_text="min length 8", min_length=8
    )

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'photo', 'full_name']
        read_only_fields = ['user']
        ref_name = 'ProfileSerializer'

    def update(self, instance, validated_data):
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance
