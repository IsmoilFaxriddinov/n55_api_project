from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from posts.models import PostModel, TopicModel

user = get_user_model()

class PostsSerializers(serializers.ModelSerializer):
    topics = serializers.PrimaryKeyRelatedField(queryset=TopicModel.objects.all(), many=True, required=True)
    class Meta:
        model = PostModel
        fields = '__all__'

# class PostClapsSerializer(serializers.Serializer):
