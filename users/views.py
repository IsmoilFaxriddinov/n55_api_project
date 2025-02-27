from ast import Try
import random
import threading
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate


from users.models import FollowModel
from users.serializers import FollowUserSerializer, LoginSerializer, RecendVerifyEmailSerializer, RegisterSerializer, UpdatePasswordSerializer, UserSerializer, VerifyEmailSerializer
from users.utils import get_verification_code, send_email_confirmation


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user.set_password(raw_password=serializer.validated_data['password1'])
        user.is_active = False
        user.save()


        code = get_verification_code(user=user)

        verification_code = str(random.randint(1000, 9999))

        email_thread = threading.Thread(target=send_email_confirmation, args=(user, verification_code))
        email_thread.start()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

class VerifyEmailAPIView(APIView):
    serailizer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.serailizer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_code = serializer.validated_data.get('user_code')

        user_code.user.is_active = True
        user_code.user.save()
        tokens = user_code.user.get_tokens()
        user_code.delete()
        
        return Response(data=tokens, status=status.HTTP_200_OK)
    
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

class ResendVerificationCodeAPIView(APIView):
    serailizer_class = RecendVerifyEmailSerializer

    def post(self, request):
        serializer = self.serailizer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(data={"success": True, "detail": "Code is send"}, status=status.HTTP_200_OK)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        tokens = user.get_tokens()

        return Response(data=tokens, status=status.HTTP_200_OK)
    
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        serializer = self.serializer_class(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
     
class UpdatePasswordAPIView(APIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        authenticated_user = authenticate(username=user.username, password=serializer.validated_data['old_password'])
        if authenticated_user is None:
            raise serializers.ValidationError("Old passsword is invalid ⚠️")
        user.set_password(raw_password=serializer.validated_data['new_password1'])
        user.save()
        return Response(data={'detail': "Password updated"}, status=status.HTTP_202_ACCEPTED)
    
class FollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUserSerializer

    def post(self, request, *args, **kwargs):
        response = dict()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        from_user = request.user
        to_user = serializer.validated_data['to_user']
        if from_user == to_user:
            raise ValidationError("You can not follow to userself !")
        follow_status = FollowModel.objects.filter(from_user=from_user, to_user=to_user)
        if follow_status.exists():
            follow_status.filter().first().delete()
            response['detail'] = "User unfollow"
            response['status'] = "unfollowed"
            return Response(data=response, status=status.HTTP_204_NO_CONTENT)
        else:
            FollowModel.objects.create(from_user=from_user, to_user=to_user)
            response['detail'] = "User followed to this user"
            response['status'] = "folloed"
            return Response(data=response, status=status.HTTP_201_CREATED)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        follow_type = request.query_params.get('type')
        if follow_type not in ['followers', 'following']:
            raise ValidationError("Invalid Query params !")
        if follow_type == "following":
            users = [user.to_user for user in request.user.following.all()]
        else:
            users = [user.from_user for user in request.user.followers.all()]

        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)