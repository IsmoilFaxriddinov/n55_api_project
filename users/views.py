from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from users.serializers import LoginSerializer
from users.utils import get_tokens_for_user

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data('user')
        tokens = get_tokens_for_user(user=user)
        return Response(data=tokens, status=status.HTTP_200_OK)
