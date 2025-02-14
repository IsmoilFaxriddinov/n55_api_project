from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenBlacklistView)

from users.views import LoginAPIView

app_name = 'users'

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
