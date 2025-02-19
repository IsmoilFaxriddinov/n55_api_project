import random
import threading
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.serializers import LoginSerializer, RegisterSerializer, VerifyEmailSerializer
from users.utils import send_email_confirmation


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user.set_password(raw_password=serializer.validated_data['password1'])
        user.is_active = False
        user.save()

        verification_code = str(random.randint(1000, 9999))

        email_thread = threading.Thread(target=send_email_confirmation, args=(user, verification_code))
        email_thread.start()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

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

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data('user')
        tokens = user.get_tokens(user=user)

        return Response(data=tokens, status=status.HTTP_200_OK)
