from django.urls import path

from posts.views import PostAPIView, PostDetailAPIView

app_name = 'posts'

urlpatterns = [
    path('', PostAPIView.as_view(), name='list'),
    path("<slug:slug>/", PostDetailAPIView.as_view(), name="detail"),
    path("me/", PostDetailAPIView.as_view(), name="my-posts"),
    path("<slug:slug>/claps/", PostDetailAPIView.as_view(), name="claps"),
    path("<slug:slug>/comments/", PostDetailAPIView.as_view(), name="claps"),
    path("<slug:slug>/comments/claps/", PostDetailAPIView.as_view(), name="claps"),
]
