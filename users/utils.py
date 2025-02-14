from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import datetime, timedelta

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh.set_exp(from_time=timezone.now(), lifetime=timedelta(minutes=1))
    # refresh.access_token.set_exp(from_time=timezone.now(), lifetime=timedelta(minutes=1))

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }