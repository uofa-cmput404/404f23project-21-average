from django.shortcuts import render
from rest_framework import permissions, pagination, viewsets
from .models import *
from .serializers import *
from django.db.models import Q

# Create your views here.


class Pagination(pagination.PageNumberPagination):
    page_size = 10


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Filter posts based on shared_with_friends and user relationship
            return Post.objects.filter(
                Q(shared_with_friends=False) | Q(owner__followers=user.author)
            )
        return Post.objects.filter(shared_with_friends=False)

#Checks whether a user has permission to access a post based on the shared_with_friends attribute and the user's relationship with the author.
class IsSharedWithFriends(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.shared_with_friends and user.is_authenticated:
            # Check if the user is a friend/follower of the author
            return user.author.followers.filter(id=obj.owner.id).exists()
        return not obj.shared_with_friends

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,IsSharedWithFriends]
    pagination_class = Pagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination


class ConnectedNodeViewSet(viewsets.ModelViewSet):
    queryset = ConnectedNode.objects.all()
    serializer_class = ConnectedNodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
