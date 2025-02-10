from django.urls import path

from posts.views import post_detail_view, post_view

app_name = 'posts'

urlpatterns = [
    path('', post_view, name='list'),
    path("<slug:slug>/", post_detail_view, name="detail")
]
