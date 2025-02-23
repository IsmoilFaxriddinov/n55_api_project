from django.urls import path

from posts.views import PersonalListView, PostAPIView, PostClapsAPIView, PostCommentListAPIView, PostDetailAPIView, PostRetrieveUpdateDestroyAPIView

app_name = 'posts'

urlpatterns = [
    path('', PostAPIView.as_view(), name='list'),
    path("me/", PersonalListView.as_view(), name="my-posts"),
    path("<slug:slug>/", PostRetrieveUpdateDestroyAPIView.as_view(), name="detail"),

    path("<slug:slug>/claps/", PostClapsAPIView.as_view(), name="claps"),
    path("<slug:slug>/comments/", PostCommentListAPIView.as_view(), name="comments"),
    path("<slug:slug>/comments/claps/", PostDetailAPIView.as_view(), name="claps"),
]
