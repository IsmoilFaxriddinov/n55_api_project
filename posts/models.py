from django.db import models
from django.contrib.auth.models import User

class PostModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(unique=True, null=True)
    title = models.CharField(max_length=125)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        slug = 
        return super().save(**kwargs)

    def __str__(self):
        return self.title
