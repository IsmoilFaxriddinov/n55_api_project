from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

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
        