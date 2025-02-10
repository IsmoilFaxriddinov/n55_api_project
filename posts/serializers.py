from rest_framework import serializers
from django.contrib.auth.models import User

from posts.models import PostModel


class PostsSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    title = serializers.CharField()
    body = serializers.CharField(allow_blank=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return PostModel.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.body = validated_data.get('body')
        instance.author = validated_data.get('author')
        instance.save()
        return instance