from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response

from posts.models import PostModel
from posts.serializers import PostsSerializers

@api_view(["GET", "POST"])
def posts_view(request):
    if request.method == "GET":
        posts = PostModel.objects.all()
        serializer = PostsSerializers(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = PostsSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "PUT", "DELETE"])
def post_detail_view(request, slug):
    response = {"success": True}
    try:
        post = PostModel.objects.get(slug=slug)
    except PostModel.DoesNotExist:
        response["success"] = False
        response["detail"] = "Post does not found"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostsSerializers(post)
        response["data"] = serializer.data
        return Response(data=response, status=status.HTTP_200_OK)

    elif request.method == "PUT" or request.method == "PATCH":
        if request.method == "PUT":
            serializer = PostsSerializers(post, data=request.data)
        else:
            serializer = PostsSerializers(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            response["data"] = serializer.data
            return Response(data=response, status=status.HTTP_202_ACCEPTED)
        else:
            response["detail"] = "Your data is not valid"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        post.delete()
        response["detail"] = "Post is deleted"
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)


class PostAPIView(APIView):
    serializer_class = PostsSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        posts = PostModel.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostDetailAPIView(APIView):
    serializer_class = PostsSerializers

    def get(self, request, slug):
        post = self.get_object(slug=slug)
        serializer = self.serializer_class(post)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, slug):
        post = self.get_object(slug=slug)
        serializer = PostsSerializers(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_202_ACCEPTED)

        return Response(data={
            "success": False,
            "detail": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug):
        post = self.get_object(slug=slug)
        serializer = PostsSerializers(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data={
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_202_ACCEPTED)
    

        return Response(data={
            "success": False,
            "detail": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        post = self.get_object(slug=slug)
        post.delete()
        return Response(data={
            "success": True,
            "detail": "Post is deleted"
        }, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_object(slug):
        try:
            return PostModel.objects.get(slug=slug)
        except PostModel.DoesNotExist:
            raise NotFound({
                "success": False,
                "detail": "Post does not found"
            })

