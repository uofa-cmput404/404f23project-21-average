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

# Create your views here.


class Pagination(pagination.PageNumberPagination):
    page_size = 5


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    def get(self, request, author_pk, format=None):
        posts = Post.objects.filter(owner=author_pk)
        page = self.paginate_queryset(posts)
        return self.get_paginated_response(PostSerializer(page, many=True).data)    
        # serializer = PostSerializer(posts, many=True)
        # print('sfsndfjsdfnljsdf')
        # response = super(PostList, self).get(request)
        # return response


    def post(self, request, author_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(owner=author)
            print(PostSerializer(post))
            return Response(PostSerializer(post), status=status.HTTP_201_CREATED)
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

    def post(self, request, author_pk, post_pk, format=None):
        print(request.data, author_pk, post_pk,  'afaq')
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=author, id=post_pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(owner=author, id=post_pk)
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, author_pk, post_pk, format=None):
        post = self.get_object(post_pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def delete(self, request, author_pk, post_pk, format=None):
        post = self.get_object(post_pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    def get(self, request, author_pk, post_pk, format=None):
        comments = Comment.objects.filter(parentPost=post_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(commenter=author, parentPost=post)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
