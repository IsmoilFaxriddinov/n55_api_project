from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

from app_common.models import BaseModel

class TopicModel(BaseModel):
    title = models.CharField(max_length=125)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'topic'
        verbose_name_plural = 'topics'

class PostModel(BaseModel):
    image = models.ImageField(upload_to='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(unique=True, null=True)
    title = models.CharField(max_length=125)
    short_description = models.CharField(max_length=255)
    body = models.TextField()
    topics = models.ManyToManyField(TopicModel, related_name='posts')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class PostClapModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='post_claps', null=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='claps')

    def __str__(self):
        return f"{self.post.id} clapped by {self.user.username}"
    
    class Meta:
        verbose_name = 'post clap'
        verbose_name_plural = 'post claps'


class PostCommentModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='post_comments', null=True)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return f"{self.user.username} comment to {self.post.id} like {self.comment}"
    
    class Meta:
        verbose_name = 'post comment'
        verbose_name_plural = 'post comments'

class PostCommentClapModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='post_comments_claps', null=True)
    comment = models.ForeignKey(PostCommentModel, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.comment.comment} clapped by {self.user.username}"
    
    class Meta:
        verbose_name = 'post comment clap'
        verbose_name_plural = 'post comments claps'