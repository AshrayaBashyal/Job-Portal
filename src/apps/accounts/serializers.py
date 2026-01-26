from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "role", "username"]

    def create(self, validated_data):
        from apps.accounts.services import register_user
        return register_user(**validated_data)    