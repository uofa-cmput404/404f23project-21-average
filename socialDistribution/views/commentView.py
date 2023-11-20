from rest_framework import permissions
from rest_framework.response import Response
from socialDistribution.models import Author, Comment, Post
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import CommentSerializer
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema


class CommentViewSet(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    @extend_schema(
        tags=['Comments'],
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
        comments = Comment.objects.filter(parentPost=post_pk)
        page = self.paginate_queryset(comments)
        serializer = CommentSerializer(comments, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        tags=['Comments'],
        
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
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(commenter=author, parentPost=post)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
