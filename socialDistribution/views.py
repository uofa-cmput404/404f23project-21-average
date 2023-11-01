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
from django.contrib.auth import get_user_model

# Create your views here.


class Pagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'


# Checks whether a user has permission to access a post based on the shared_with_friends attribute and the user's relationship with the author.
class IsSharedWithFriends(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.shared_with_friends and user.is_authenticated:
            # Check if the user is a friend/follower of the author
            return user.author.followers.filter(id=obj.owner.id).exists()
        return not obj.shared_with_friends


class AuthorListViewSet(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination
    paginate_by_param = 'page_size'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     user = get_user_model()
    #     all_users = user.objects.all()
    #     # query = Author.objects.all()
    #     serializer = CurrentUserSerializer(all_users, many=True)
    #     return Response(serializer.data)

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated:
    #         # Filter posts based on shared_with_friends and user relationship
    #         return Post.objects.filter(
    #             Q(shared_with_friends=False) | Q(owner__followers=user.author)
    #         )
    #     return Post.objects.filter(shared_with_friends=False)


class AuthorDetailView(APIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    @extend_schema(
        tags=['authors'],
    )
    def get(self, request, author_pk, format=None):
        author = get_object_or_404(Author, pk=author_pk)
        serializer_context = {
            'request': request,
        }
        serializer = AuthorSerializer(author, context=serializer_context)
        return Response(serializer.data)

    @extend_schema(
        tags=['authors'],
    )
    def post(self, request, author_pk, format=None):
        author = get_object_or_404(Author, pk=author_pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


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


class AddLikeToPostView(APIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    @extend_schema(
        tags=['Likes'],
    )
    def get(self, request, author_pk, post_pk, format=None):
        post = Post.objects.get(pk=post_pk)
        likes = PostLike.objects.filter(post=post)
        serializer = PostLikeSerializer(likes, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['Likes'],
    )
    def post(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk)

        # check if author already liked the post
        if PostLike.objects.filter(author=author, post=post).exists():
            return Response({"message": "cannot like post again"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid():
            like = serializer.save(author=author, post=post)
            return Response(PostLikeSerializer(like).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddLikeToCommentView(APIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    @extend_schema(
        tags=['Likes'],
    )
    def post(self, request, author_pk, post_pk, comment_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        comment = Comment.objects.get(pk=comment_pk)

        # check if author already liked the post
        if CommentLike.objects.filter(author=author, comment=comment).exists():
            return Response({"message": "cannot like comment again"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentLikeSerializer(data=request.data)
        if serializer.is_valid():
            like = serializer.save(author=author, comment=comment)
            return Response(CommentLikeSerializer(like).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Likes'],
    )
    def get(self, request, author_pk, post_pk, comment_pk, format=None):
        comment = Comment.objects.get(pk=comment_pk)
        likes = CommentLike.objects.filter(comment=comment)
        serializer = CommentLikeSerializer(likes, many=True)
        return Response(serializer.data)


class GetAllAuthorLikes(generics.ListAPIView):
    queryset1 = PostLike.objects.all()
    queryset2 = CommentLike.objects.all()
    serializer_class1 = PostLikeSerializer
    serializer_class2 = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @extend_schema(
        tags=['Likes'],
    )
    def get(self, request, author_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        posts = Post.objects.filter(owner=author)
        likes = PostLike.objects.filter(author=author)
        likes2 = CommentLike.objects.filter(author=author)
        serializer = PostLikeSerializer(likes, many=True)
        serializer2 = CommentLikeSerializer(likes2, many=True)
        return Response(serializer.data+serializer2.data)


class ImageViewSet(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    def get(self, request, author_pk, post_pk, format=None):
        post = Post.objects.get(pk=post_pk)
        if post.imageOnlyPost:
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


class ConnectedNodeViewSet(viewsets.ModelViewSet):
    queryset = ConnectedNode.objects.all()
    serializer_class = ConnectedNodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination
