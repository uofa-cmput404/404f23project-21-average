import requests
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
from socialDistribution.util import sendToFriendsInbox, isFriend
import base64
from io import BytesIO
from PIL import Image
from django.http import HttpResponse
from socialDistribution.util import addToInbox


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsSharedWithFriends]
    pagination_class = Pagination

    @extend_schema(
        tags=['Posts'],
        description='[local, remote] get the recent posts from author AUTHOR_ID (paginated)'
    )
    def get(self, request, author_pk, format=None):
        # TODO: check permissions fo requsting author and return only relevant posts to them
        posts = Post.objects.filter(owner=author_pk)
        for post in posts:
            post.source = request.headers['Host'] + '/authors/' + str(post.owner.id) + '/posts/' + str(post.id)
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
            serializer.save(owner=author, origin=request.headers['Origin'])
            # TODO: Check if the post is sent to all friends inbox if its friends only
            sendToFriendsInbox(author, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
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
        post = Post.objects.get(pk=post_pk, owner=author)
        if post:
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
            serializer.save(owner=author, id=post_pk)
            sendToFriendsInbox(author, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Posts'],
    )
    def get(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        post = self.get_object(post_pk)
        serializer = PostSerializer(post)
        print(post.visibility)
        if post.owner.id == author.id:
            return Response(serializer.data)
        if post.visibility == 'FRIENDS' and isFriend(author, post.owner):
            return Response(serializer.data)
        # TODO: CHECK IF PERMISSION IS CORRECT
        if post.visibility == 'PUBLIC':
            return Response(serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)

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
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @extend_schema(
        tags=['Posts'],
    )
    def get(self, request, author_pk, post_pk, format=None):
        post = Post.objects.get(pk=post_pk)
        if post.imageOnlyPost:
            # https://stackoverflow.com/questions/31826335/how-to-convert-pil-image-image-object-to-base64-string
            if post.image_link:
                im = Image.open(requests.get(post.image_link, stream=True).raw)
                buffered = BytesIO()
                im.save(buffered, format="JPEG")
                base64_data = base64.b64encode(buffered.getvalue())
            elif post.image:
                with open(post.image.path, "rb") as img_file:
                    base64_data = base64.b64encode(img_file.read())
            return HttpResponse(base64_data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
