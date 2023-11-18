from django.urls import path, include
# from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import AddLikeToCommentView, AddLikeToPostView, AuthorDetailView, AuthorListViewSet, GetAllAuthorLikes, \
    ImageViewSet, PostDetail, PostList, CommentViewSet, FollowViewSet, FriendRequestViewSet, ConnectedNodeViewSet, InboxItemView

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # authors
    path('authors/',
         AuthorListViewSet.as_view(), name='authors-list'),
    path('authors/<slug:author_pk>/',
         AuthorDetailView.as_view(), name='authors'),

    # posts
    path('authors/<slug:author_pk>/posts/',
         PostList.as_view(), name='posts-list'),
    path('authors/<slug:author_pk>/posts/<slug:post_pk>',
         PostDetail.as_view(), name='posts-detail'),

    # comments
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/comments/',
         CommentViewSet.as_view(), name='comments'),
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/image',
         ImageViewSet.as_view(), name='image'),
    # likes
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/likes/',
         AddLikeToPostView.as_view(), name='likes'),
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/comments/<slug:comment_pk>/likes/',
         AddLikeToCommentView.as_view(), name='likes'),
    #     path('authors/<slug:author_pk>/liked/',
    #          GetAllAuthorLikes.as_view(), name='likes'),
    # inbox
    path('inbox/', InboxItemView.as_view(), name='inbox'),
]
