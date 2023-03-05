from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.constants import Role

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        attrs["password"] = make_password(attrs["password"])
        attrs["role"] = Role.USER

        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "role"]
        extra_kwargs = {
            "email": {"read_only": True},
            "role": {"read_only": True},
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        attrs["password"] = make_password(attrs["password"])

        return attrs


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "role"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "is_staff", "is_superuser", "user_permissions"]
