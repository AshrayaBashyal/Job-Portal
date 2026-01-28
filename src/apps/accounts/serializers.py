from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "role", "role_display", "username"]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6},
            'username': {'required': False, 'allow_blank': True},
            'email': {'required': True}
        }
    
    def create(self, validated_data):
        from apps.accounts.services import register_user
        return register_user(**validated_data)    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)    
        # self.user is available here because it's a login
        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "role": self.user.role,
            "role_display": self.user.get_role_display()
        }
        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # If rotation ON → use new token
        # If rotation OFF → reuse old one from request
        refresh_token = data.get("refresh") or attrs["refresh"]
        refresh = RefreshToken(refresh_token)

        user_id = refresh.payload.get("user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User no longer exists."})
        
        # Use 'user' (local variable), not 'self.user'
        data["user"] = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "role_display": user.get_role_display()
        }        
        
        return data