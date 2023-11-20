from django.urls import path
from socialDistribution.views import InboxItemView

from socialDistribution.views.authorView import AuthorListViewSet, AuthorDetailView
from socialDistribution.views.commentView import CommentViewSet
from socialDistribution.views.followerView import FollowDetailViewSet, FollowViewSet
from socialDistribution.views.likesView import AddLikeToCommentView, AddLikeToPostView
from socialDistribution.views.postView import ImageViewSet, PostList, PostDetail

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
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/',
         PostDetail.as_view(), name='posts-detail'),

    # comments
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/comments/',
         CommentViewSet.as_view(), name='comments'),
    
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/image/',
         ImageViewSet.as_view(), name='image'),
   
    # likes
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/likes/',
         AddLikeToPostView.as_view(), name='post-likes'),
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/comments/<slug:comment_pk>/likes/',
         AddLikeToCommentView.as_view(), name='comment-likes'),
    
    # followers
    path('authors/<slug:author_pk>/followers/', FollowViewSet.as_view(), name='followers'),
    path('authors/<slug:author_pk>/followers/<slug:foreign_author_pk>/', FollowDetailViewSet.as_view(), name='followers-detail'),

     # inbox
    path('inbox/', InboxItemView.as_view(), name='inbox'),
]
