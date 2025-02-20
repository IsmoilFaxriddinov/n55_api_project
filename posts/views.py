from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

from posts.models import PostModel
from posts.serializers import PostsSerializers

class PostAPIView(APIView):
    serializer_class = PostsSerializers
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        print(request.user)
        print(request.auth)
        print(request.auth.get('username'))
        print(request.auth.get('n55'))
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

