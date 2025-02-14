from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['n55'] = "salomat 😀"

        return token

class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('email_or_username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=email_or_username)
        except User.DoesNotExist:
            user = User.objects.get(email=email_or_username)

        
        if user is None:
            raise serializers.ValidationError({
                "success": False,
                "detail": "User does not found with this email or passsword"
            })
        authenticated_user = authenticate(username=user.username, password=password)
        if authenticated_user is None:
            raise serializers.ValidationError({
                "success": False,
                "detail": "Username or passsword is invalid"
            })
        
        attrs['user'] = authenticated_user
        return authenticated_user