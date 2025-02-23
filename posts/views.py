from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from django.db.models import Count
from django.contrib.auth import get_user_model

from app_common.paginations import StandardResultsSetPagination
from app_common.permissions import IsOwnerOrReadOnly
from posts.models import PostClapModel, PostModel
from posts.serializers import PostClapsUserSerializer, PostsSerializers

User = get_user_model()

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

class PostClapsAPIView(APIView):
    serializer_class = PostClapsUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request, slug):
        post = self.get_object(slug=slug)
        claps = PostClapModel.objects.filter(post=post)
        claps_count = claps.count()
        users = claps.values('post', 'user').annotate(count=Count('id'))
        users_count = users.count()

        users_id_list = set()   
        for user in users.values('user_id'):
            users_id_list.add(user['user_id'])
        users_object = User.objects.filter(id__in=users_id_list).order_by('-id')

        paginator = self.pagination_class()
        paginated_posts = paginator.paginate_queryset(users_object, request)
        serializer = self.serializer_class(paginated_posts, many=True)
        return Response(data={"claps_count": claps_count, 'users_count': users_count, "users": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request, slug):
        post = self.get_object(slug=slug)
        user = request.user

        PostClapModel.objects.create(user=user, post=post)

        claps_count = PostClapModel.objects.filter(post=post).count()
    
        return Response(data={"claps_count": claps_count}, status=status.HTTP_201_CREATED)

    
    def get_claps_count(self, post):
        return PostClapModel.objects.create(user=self.request.user, post=post)


    @staticmethod
    def get_object(slug):
        try:
            return PostModel.objects.get(slug=slug)
        except PostModel.DoesNotExist:
            raise ValidationError("Post does not exists")
    
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)