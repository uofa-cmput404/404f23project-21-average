from django.shortcuts import get_object_or_404, render
from rest_framework import permissions, pagination, viewsets
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import mixins
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import generics
from django.db.models import Q
from drf_spectacular.utils import extend_schema

# Create your views here.


class Pagination(pagination.PageNumberPagination):
    page_size = 5


# Checks whether a user has permission to access a post based on the shared_with_friends attribute and the user's relationship with the author.
class IsSharedWithFriends(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.shared_with_friends and user.is_authenticated:
            # Check if the user is a friend/follower of the author
            return user.author.followers.filter(id=obj.owner.id).exists()
        return not obj.shared_with_friends


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated:
    #         # Filter posts based on shared_with_friends and user relationship
    #         return Post.objects.filter(
    #             Q(shared_with_friends=False) | Q(owner__followers=user.author)
    #         )
    #     return Post.objects.filter(shared_with_friends=False)


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsSharedWithFriends]
    pagination_class = Pagination

    @extend_schema(
        tags=['Posts'],
    )
    def get(self, request, author_pk, format=None):
        posts = Post.objects.filter(owner=author_pk)
        page = self.paginate_queryset(posts)
        return self.get_paginated_response(PostSerializer(page, many=True).data)

    @extend_schema(
        tags=['Posts'],
    )
    def post(self, request, author_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(owner=author)
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    @extend_schema(
        tags=['Posts'],
    )
    def post(self, request, author_pk, post_pk, format=None):
        print(request.data, author_pk, post_pk,  'afaq')
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=author, id=post_pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Posts'],
    )
    def put(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(owner=author, id=post_pk)
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Posts'],
    )
    def get(self, request, author_pk, post_pk, format=None):
        post = self.get_object(post_pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    @extend_schema(
        tags=['Posts'],
    )
    def delete(self, request, author_pk, post_pk, format=None):
        post = self.get_object(post_pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    @extend_schema(
        tags=['Comments'],
    )
    def get(self, request, author_pk, post_pk, format=None):
        comments = Comment.objects.filter(parentPost=post_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['Comments'],
    )
    def post(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(commenter=author, parentPost=post)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSet(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    def get(self, request, author_pk, post_pk, format=None):
        post = Post.objects.get(pk=post_pk)
        serializer = PostSerializer(post)
        return Response(serializer.data.get('image_link'))


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination


class ConnectedNodeViewSet(viewsets.ModelViewSet):
    queryset = ConnectedNode.objects.all()
    serializer_class = ConnectedNodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination
