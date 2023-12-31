from django.urls import path
from socialDistribution.views.authorView import AuthorListViewSet, AuthorDetailView, NodeListViewSet
from socialDistribution.views.commentView import CommentViewSet
from socialDistribution.views.followerView import FollowDetailViewSet, FollowViewSet, FollowingViewSet
from socialDistribution.views.githubView import GitHubView
from socialDistribution.views.inboxView import InboxItemView
from socialDistribution.views.likesView import AddLikeToCommentView, AddLikeToPostView, GetAllAuthorLikes
from socialDistribution.views.postView import ImageViewSet, PostList, PostDetail
from socialDistribution.views.streamPostsView import StreamPostList
from socialDistribution.views.shareView import ShareView

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # authors
    path('authors/',
         AuthorListViewSet.as_view(), name='authors-list'),
    path('authors/<slug:author_pk>/',
         AuthorDetailView.as_view(), name='authors'),
     path('nodes/', NodeListViewSet.as_view(), name='nodes'),

    # posts
    path('authors/<slug:author_pk>/posts/',
         PostList.as_view(), name='posts-list'),
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/',
         PostDetail.as_view(), name='posts-detail'),
     path('posts/<slug:post_pk>/image/',
         ImageViewSet.as_view(), name='image'),

    # comments
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/comments/',
         CommentViewSet.as_view(), name='comments'),
   
    # likes
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/likes/',
         AddLikeToPostView.as_view(), name='post-likes'),
    path('authors/<slug:author_pk>/posts/<slug:post_pk>/comments/<slug:comment_pk>/likes/',
         AddLikeToCommentView.as_view(), name='comment-likes'),
     path('posts/<slug:author_pk>/liked/',
         GetAllAuthorLikes.as_view(), name='liked-posts'),
    
    # followers
    path('authors/<slug:author_pk>/followers/', FollowViewSet.as_view(), name='followers'),
    path('authors/<slug:author_pk>/following/', FollowingViewSet.as_view(), name='followers-detail'),
    path('authors/<slug:author_pk>/followers/<slug:foreign_author_pk>/', FollowDetailViewSet.as_view(), name='followers-detail'),
    
    # github 
    path('authors/<slug:author_pk>/github/', GitHubView.as_view(), name='github'),
    
    # inbox
    path('authors/<slug:author_pk>/inbox/', InboxItemView.as_view(), name='inbox'),

    path('authors/<slug:author_pk>/posts/allposts/stream/', StreamPostList.as_view(), name='posts-stream'),

    path('share/<slug:post_pk>/', ShareView.as_view(), name='share-post'),
]
