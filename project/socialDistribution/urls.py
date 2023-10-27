from django.urls import path, include
# from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, PostViewSet, CommentViewSet, FollowViewSet, FriendRequestViewSet, LikeViewSet, ConnectedNodeViewSet
from rest_framework_nested import routers

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'posts',
                PostViewSet, basename='posts')
router.register(r'comment',
                CommentViewSet, basename='comment')
router.register(r'like',
                LikeViewSet, basename='like')
router.register(r'followers', FollowViewSet, basename='followers')
router.register(r'friend-request', FriendRequestViewSet,
                basename='friend-request')
router.register(r'connected-node', ConnectedNodeViewSet,
                basename='connected-node')

posts_router = routers.NestedSimpleRouter(
    router, r'authors', lookup='post')
posts_router.register(r'posts', PostViewSet, basename='post-comments')

comments_router = routers.NestedSimpleRouter(
    posts_router, r'posts', lookup='comment')
comments_router.register(r'comments', CommentViewSet, basename='comments')

likes_router = routers.NestedSimpleRouter(
    posts_router, r'posts', lookup='like')
likes_router.register(r'likes', LikeViewSet, basename='likes')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    path('', include(comments_router.urls)),
    path('', include(likes_router.urls)),
]
