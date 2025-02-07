from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from posts.models import PostModel
from posts.serializers import PostsSerializers


@api_view(['GET', 'POST'])
def post_view(request):
    if request.method == 'GET':
        posts = PostModel.objects.all()
        serializer = PostsSerializers(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = PostsSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
