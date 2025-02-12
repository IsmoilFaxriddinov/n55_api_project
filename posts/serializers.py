from rest_framework import serializers
from django.contrib.auth.models import User

from posts.models import PostModel, TopicModel


class PostsSerializers(serializers.ModelSerializer):
    topics = serializers.PrimaryKeyRelatedField(queryset=TopicModel.objects.all(), many=True, required=True)
    class Meta:
        model = PostModel
        fields = '__all__'
