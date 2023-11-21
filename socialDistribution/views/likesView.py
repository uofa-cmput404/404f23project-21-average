from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from socialDistribution.models import Author, Comment, CommentLike, Post, PostLike
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import CommentLikeSerializer, PostLikeSerializer


class AddLikeToPostView(generics.ListCreateAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @extend_schema(
        tags=['Likes'],
    )
    def get(self, request, author_pk, post_pk, format=None):
        """_summary_

        Args:
            request (_type_): _description_
            author_pk (_type_): _description_
            post_pk (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        post = Post.objects.get(pk=post_pk)
        likes = PostLike.objects.filter(post=post)
        page = self.paginate_queryset(likes)
        serializer = PostLikeSerializer(likes, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        tags=['Likes'],
    )
    def post(self, request, author_pk, post_pk, format=None):
        """_summary_

        Args:
            request (_type_): _description_
            author_pk (_type_): _description_
            post_pk (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
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


class AddLikeToCommentView(generics.ListCreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @extend_schema(
        tags=['Likes'],
    )
    def post(self, request, author_pk, post_pk, comment_pk, format=None):
        """_summary_

        Args:
            request (_type_): _description_
            author_pk (_type_): _description_
            post_pk (_type_): _description_
            comment_pk (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
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
        """_summary_

        Args:
            request (_type_): _description_
            author_pk (_type_): _description_
            post_pk (_type_): _description_
            comment_pk (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        comment = Comment.objects.get(pk=comment_pk)
        likes = CommentLike.objects.filter(comment=comment)
        page = self.paginate_queryset(likes)
        serializer = CommentLikeSerializer(likes, many=True)
        return self.get_paginated_response(serializer.data)


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
        """_summary_
        Args:
            request (_type_): _description_
            author_pk (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        author = Author.objects.get(pk=author_pk)
        posts = Post.objects.filter(owner=author)
        likes = PostLike.objects.filter(author=author)
        likes2 = CommentLike.objects.filter(author=author)
        serializer = PostLikeSerializer(likes, many=True)
        serializer2 = CommentLikeSerializer(likes2, many=True)
        return Response(serializer.data+serializer2.data)
