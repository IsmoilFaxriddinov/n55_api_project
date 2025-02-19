import random
from django.db import models
from app_common.models import BaseModel
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserModel(AbstractUser):
    email = models.EmailField(unique=True)
    
    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        # refresh.set_exp(from_time=timezone.now(), lifetime=timedelta(minutes=1))
        # refresh.access_token.set_exp(from_time=timezone.now(), lifetime=timedelta(minutes=1))

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def get_verification(self, expire_minutes=2):
        code = random.randint(1000, 9999)
        user_code = VerificationModel.objects.filter(user=self, code=code)
        if user_code.exists():
            user_code.delete()
            self.get_verification_code()
        VerificationModel.objects.create(user=self, code=code, expire_minutes=expire_minutes)
        return code
            

User = get_user_model()

class VerificationModel(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='code')
    code = models.PositiveSmallIntegerField()
    expire_minutes = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.code)
    
    class Meta:
        verbose_name = 'code'
        verbose_name_plural = 'codes'

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile', null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif'])])
    short_bio = models.CharField(max_length=160, null=True)
    about = models.TextField()
    pronouns = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
