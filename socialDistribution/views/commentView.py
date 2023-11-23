from rest_framework import permissions
from rest_framework.response import Response
from socialDistribution.models import Author, Comment, Post
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import CommentSerializer
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from ..util import addToInbox


class CommentViewSet(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @extend_schema(
        tags=['Comments'],
    )
    def get(self, request, author_pk, post_pk, format=None):
        comments = Comment.objects.filter(parentPost=post_pk)
        page = self.paginate_queryset(comments)
        serializer = CommentSerializer(comments, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        tags=['Comments'],
    )
    def post(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author, parentPost=post)

            # add the comment to post owners inbox
            addToInbox(post.owner, serializer.data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
