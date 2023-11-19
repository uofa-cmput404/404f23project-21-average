from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from socialDistribution.models import Author, Post
from socialDistribution.pagination import Pagination
from socialDistribution.permissions import IsSharedWithFriends
from socialDistribution.serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsSharedWithFriends]
    pagination_class = Pagination

    @extend_schema(
        tags=['Posts'],
        description='[local, remote] get the recent posts from author AUTHOR_ID (paginated)'
    )
    def get(self, request, author_pk, format=None):
        posts = Post.objects.filter(owner=author_pk)
        page = self.paginate_queryset(posts)
        return self.get_paginated_response(PostSerializer(page, many=True).data)

    @extend_schema(
        tags=['Posts'],
        description='Create a new post but generate a new id'
    )
    def post(self, request, author_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid():
            post = serializer.save(owner=author, origin=request.headers['Origin'])
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
        description='Update the post whose id is POST_ID (must be authenticated)'
    )
    def post(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=author, id=post_pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Posts'],
        description='create a post where its id is POST_ID'
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
        description='Delete a post'
    )
    def delete(self, request, author_pk, post_pk, format=None):
        post = self.get_object(post_pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageViewSet(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    @extend_schema(
        tags=['Posts'],
    )
    def get(self, request, author_pk, post_pk, format=None):
        post = Post.objects.get(pk=post_pk)
        if post.imageOnlyPost:
            serializer = PostSerializer(post)
            return Response(serializer.data.get('image_link'))
