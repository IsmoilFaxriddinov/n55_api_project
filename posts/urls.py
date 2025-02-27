from email.mime import base
from rest_framework.routers import DefaultRouter
from django.urls import path

from posts.views import (CommentChildrenListAPIView, CommentClapsListCreateAPIView,
                        PersonalListView, PostAPIView, PostClapsAPIView, PostCommentListCreateAPIView,
                        PostRetrieveUpdateDestroyAPIView, TopicViewSet)

app_name = 'posts'

router = DefaultRouter()
router.register(r'topics', TopicViewSet)

urlpatterns = router.urls

urlpatterns += [
    # old urls
    path('', PostAPIView.as_view(), name='list'),
    path("me/", PersonalListView.as_view(), name="my-posts"),
    path("<slug:slug>/", PostRetrieveUpdateDestroyAPIView.as_view(), name="detail"),
    path("<slug:slug>/claps/", PostClapsAPIView.as_view(), name="claps"),

    # new urls
    path("<slug:slug>/comments/", PostCommentListCreateAPIView.as_view(), name="claps"),
    path("comments/<int:pk>/", CommentChildrenListAPIView.as_view(), name="comments_children"),
    path("comments/<int:pk>/claps", CommentClapsListCreateAPIView.as_view(), name="claps")
] + router.urls


