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
    

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def post_detail_view(request, slug):
    response = {'success': True}
    try:
        post = PostModel.objects.get(slug=slug)
    except PostModel.DoesNotExist:
        response['success'] = False
        response['detail'] = "Post does not exists ⚠️"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = PostsSerializers(post)
        response['data'] = serializer.data
        return Response(data=response, status=status.HTTP_200_OK)
    
    elif request.method == "PUT" or request.method == "PATCH":
        if request.method == "PUT":
            serializer = PostsSerializers(post, data=request.data)
        else:
            serializer = PostsSerializers(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response['data'] = serializer.data
            return Response(data=response, status=status.HTTP_202_ACCEPTED)
        else:
            response['detail'] = "Your data is not valid"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    
    elif request.method == "DELETE":
        post.delete()
        response['detail'] = "Post is deleted ✔️"
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)