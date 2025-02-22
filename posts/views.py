from urllib import request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from app_common.paginations import StandardResultsSetPagination
from app_common.permissions import IsOwnerOrReadOnly
from posts.models import PostModel
from posts.serializers import PostsSerializers

class PostAPIView(APIView):
    serializer_class = PostsSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        posts = PostModel.objects.all()
        paginator = self.pagination_class()
        paginated_posts = paginator.paginate_queryset(posts, request)

        serializer = self.serializer_class(paginated_posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def get_serialiser(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


class PostDetailAPIView(APIView):
    serializer_class = PostsSerializers
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, slug):
        post = self.get_object(slug=slug)
        self.check_object_permissions(request, post)
        serializer = self.serializer_class(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        post = self.get_object(slug=slug)
        self.check_object_permissions(request, post)
        serializer = PostsSerializers(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug):
        post = self.get_object(slug=slug)
        self.check_object_permissions(request, post)
        serializer = PostsSerializers(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
    

        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        post = self.get_object(slug=slug)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get_object(slug):
        try:
            return PostModel.objects.get(slug=slug)
        except PostModel.DoesNotExist:
            raise NotFound({
                "success": False,
                "detail": "Post does not found"
            })

class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostsSerializers
    queryset = PostModel.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]
    

class PersonalListView(ListAPIView):
    serializer_class = PostsSerializers
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    # queryset = PostModel.objects.all()

    def get_queryset(self):
        return PostModel.objects.filter(author=self.request.user)