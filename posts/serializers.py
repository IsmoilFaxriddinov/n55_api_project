from urllib import request
from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.models import PostCommentClapModel, PostCommentModel, PostModel, TopicModel

User = get_user_model()

class PostAuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.ImageField(source="profile.avatar", read_only=True)
    class Meta:
        model = User
        fields = ['full_name', 'avatar']
    
    @staticmethod
    def get_full_name(obj):
        return obj.get_full_name()


class PostsSerializers(serializers.ModelSerializer):
    topics = serializers.PrimaryKeyRelatedField(queryset=TopicModel.objects.all(), many=True, required=True, write_only=True)
    comments_count = serializers.SerializerMethodField()
    claps_count = serializers.SerializerMethodField()
    class Meta:
        model = PostModel
        fields = ['slug', 'image', 'title', 'body', 'short_description', 'topics', 'claps_count', 'comments_count', 'created_at']
        read_only_fields = ['created_at', 'slug']
    
    @staticmethod
    def get_claps_count(obj):
        return obj.claps.count()
    
    @staticmethod
    def get_comments_count(obj):
        return obj.comments.count()
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['author'] = PostAuthorSerializer(instance=instance.author).data
        return data

class PostClapsUserSerializer(serializers.ModelSerializer):
    short_bio = serializers.CharField(source="profile.short_bio")
    avatar = serializers.ImageField(source="profile.avatar")
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['short_bio', 'avatar', 'username', 'is_followed']
    
    def get_is_followed(self, obj):
        user = self.context.get('user')
        return user.following.filter(to_user_id=obj.id).exists()
    

class PostCommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = PostCommentModel
        fields = ['id', 'parent', 'comment', 'user', 'children']
    
    @staticmethod
    def get_children(obj):
        return obj.children.count()

class PostCommentClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentClapModel
        fields = []

class TopicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicModel
        fields = ['id', 'title']
