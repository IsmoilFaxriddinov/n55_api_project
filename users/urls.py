from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenBlacklistView)

from users.views import LoginAPIView, RegisterAPIView, VerifyEmailAPIView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/email/', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('resend/code/', LoginAPIView.as_view(), name='login'),
    path('me/', LoginAPIView.as_view(), name='login'),
    path('update/password/', LoginAPIView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),\
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]