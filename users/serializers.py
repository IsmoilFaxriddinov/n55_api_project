from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import VerificationModel

User = get_user_model()
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username

        return token                                                   

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 != password2:
            raise serializers.ValidationError("Passwords does not match")
        
        validate_password(password=password1)
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password1')
        validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        return user

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        try:
            user_code = VerificationModel.objects.get(user__email=email, code=code)
        except VerificationModel.DoesNotExist:
            raise serializers.ValidationError('Invalid verification code')

        current_time = timezone.now()
        expiration_time = user_code.created_at + timedelta(minutes=user_code.expire_minutes)

        if current_time > expiration_time:
            user_code.delete()
            raise serializers.ValidationError('Verification code has expired')

        attrs['user_code'] = user_code
        return attrs


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