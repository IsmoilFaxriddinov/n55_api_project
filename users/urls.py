from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenBlacklistView)

from users.views import LoginAPIView, RegisterAPIView, ResendVerificationCodeAPIView, UserProfileView, VerifyEmailAPIView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/email/', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('resend/code/', ResendVerificationCodeAPIView.as_view(), name='login'),
    path('me/', UserProfileView.as_view(), name='me'),
    path('update/password/', LoginAPIView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),\
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]