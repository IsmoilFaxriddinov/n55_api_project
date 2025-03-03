from urllib import request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.generics import (RetrieveUpdateDestroyAPIView,
                                    ListAPIView, ListCreateAPIView, get_object_or_404)
from django.db.models import Count
from django.contrib.auth import get_user_model

from app_common.paginations import LargeResultsSetPagination, StandardResultsSetPagination
from app_common.permissions import IsCommentOwner, IsOwnerOrReadOnly
from posts.models import (PostClapModel, PostCommentClapModel,
                        PostCommentModel, PostModel, TopicModel)
from posts.serializers import PostClapsUserSerializer, PostCommentClapSerializer, PostCommentSerializer, PostsSerializers, TopicModelSerializer

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
        serializer = self.serializer_class(paginated_posts, many=True, context={'user': request.user})
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


class PostCommentListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = PostCommentSerializer

    def get_queryset(self):
        post = get_object_or_404(PostModel, slug=self.kwargs['slug'])
        return PostCommentModel.objects.filter(post=post).order_by('-id')

    def perform_create(self, serializer):
        post = get_object_or_404(PostModel, slug=self.kwargs['slug'])
        return serializer.save(post=post, user=self.request.user)
    

class CommentChildrenListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCommentOwner]
    pagination_class = StandardResultsSetPagination
    serializer_class = PostCommentSerializer

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(PostCommentModel, id=self.kwargs['pk'])
        children =  PostCommentModel.objects.filter(parent=comment).order_by('-id')
        paginator = self.pagination_class()
        paginated_posts = paginator.paginate_queryset(children, self.request)
        serializer = self.serializer_class(paginated_posts, many=True)
        print(children.exists())
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        comment = get_object_or_404(PostCommentModel, id=self.kwargs['pk'])
        self.check_object_permissions(request, comment)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment.comment = serializer.validated_data['comment']
        comment.save()
        return Response(data='updated', status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        ...

class CommentClapsListCreateAPIView(ListCreateAPIView):
    serializer_class = PostClapsUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        comment = get_object_or_404(PostCommentModel, id=self.kwargs['pk'])
        PostCommentClapModel.objects.create(user=self.request.user, comment=comment)
        claps_count = PostCommentClapModel.objects.filter(user=self.request.user, comment=comment).count()
        print(claps_count)

        return Response(data={'claps_count': claps_count}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        comment = get_object_or_404(PostCommentModel, id=self.kwargs['pk'])

        claps = PostCommentClapModel.objects.filter(comment=comment)

        claps_count = claps.count()

        users_id = claps.values('user_id').annotate(count=Count('id')).values_list('user_id', flat=True)

        users = User.objects.filter(id__in=users_id).order_by('-id')

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
        else:
            serializer = self.serializer_class(users, many=True)
        return Response({"claps count": claps_count, "users_count": users.count(), "users": serializer.data})


class TopicsLIstAPIView(ListAPIView):
    queryset = TopicModel.objects.all()
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]
    serializer_class = TopicModelSerializer
    

class TopicViewSet(viewsets.ModelViewSet):
    queryset = TopicModel.objects.all()
    serializer_class = TopicModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get_permissions(self):
        if self.request.method in ["POST", "GET"]:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    