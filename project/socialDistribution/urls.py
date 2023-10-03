from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register our viewsets with it.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'author', AuthorViewSet, basename='author')
router.register(r'post', PostViewSet, basename='post')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'friendrequest', FriendRequestViewSet,
                basename='friendrequest')
router.register(r'like', LikeViewSet, basename='like')
router.register(r'connectednode', ConnectedNodeViewSet,
                basename='connectednode')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
