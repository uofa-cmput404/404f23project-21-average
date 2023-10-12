from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register our viewsets with it.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'followers', FollowViewSet, basename='followers')
router.register(r'friend-request', FriendRequestViewSet,
                basename='friend-request')
router.register(r'like', LikeViewSet, basename='like')
router.register(r'connected-node', ConnectedNodeViewSet,
                basename='connected-node')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
