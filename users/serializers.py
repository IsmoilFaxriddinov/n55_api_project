import random
import threading
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import FollowModel, VerificationModel
from users.utils import send_email_confirmation

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


class RecendVerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')

        user_code = VerificationModel.objects.filter(user__email=email).first()
        if not user_code:
            raise serializers.ValidationError('Verification code not found')

        current_time = timezone.now()
        expiration_time = user_code.created_at + timedelta(minutes=user_code.expire_minutes)

        if current_time > expiration_time:
            user = user_code.user
            user_code.delete()

            verification_code = str(random.randint(1000, 9999))
            VerificationModel.objects.create(user=user, code=verification_code, expire_minutes=5)

            email_thread = threading.Thread(target=send_email_confirmation, args=(user, verification_code))
            email_thread.start()
        else:
            raise serializers.ValidationError('You have an active code')

        attrs['user'] = user
        attrs['verification_code'] = verification_code
        return attrs


class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(max_length=125)
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


class UserSerializer(serializers.ModelSerializer):
    short_bio = serializers.CharField(source="profile.short_bio")
    avatar = serializers.ImageField(source="profile.avatar")
    about = serializers.CharField(source="profile.about")
    pronouns = serializers.CharField(source="profile.pronouns")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'short_bio', 'avatar', 'about', 'pronouns']

    def update(self, instance, validated_data):
        # Extract nested profile data
        profile_data = validated_data.pop("profile", {})

        # Update User fields if necessary
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.save()

        # Update Profile fields
        profile = instance.profile  # Get the related profile instance
        profile.short_bio = profile_data.get("short_bio", profile.short_bio)
        profile.avatar = profile_data.get("avatar", profile.avatar)
        profile.about = profile_data.get("about", profile.about)
        profile.pronouns = profile_data.get("pronouns", profile.pronouns)
        profile.save()

        return instance


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=125)
    new_password1 = serializers.CharField(max_length=125)
    new_password2 = serializers.CharField(max_length=125)

    def validate(self, attrs):
        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.get('new_password2')

        if new_password1 != new_password2:
            raise serializers.ValidationError("Passwords does not match")

        validate_password(password=new_password1)
        return attrs


class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowModel
        fields = ['to_user']
