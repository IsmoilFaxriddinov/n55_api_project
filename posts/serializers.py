from rest_framework import serializers

from posts.models import PostModel

class PostsSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'