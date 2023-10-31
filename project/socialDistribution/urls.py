from django.urls import path, include
# from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, ImageViewSet, PostDetail, PostList, CommentViewSet, FollowViewSet, FriendRequestViewSet, LikeViewSet, ConnectedNodeViewSet
from rest_framework_nested import routers

# Create a router and register our viewsets with it.

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('authors/<slug:author_pk>/posts/', PostList.as_view(), name='posts'),
    path('authors/<slug:author_pk>/posts/<slug:post_pk>', PostDetail.as_view(), name='posts'),
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/comments/', CommentViewSet.as_view(), name='comments'),
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/image', ImageViewSet.as_view(), name='image'),
]
