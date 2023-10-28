from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, pagination, viewsets
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


class Pagination(pagination.PageNumberPagination):
    page_size = 10


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]
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
