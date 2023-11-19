from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Post
from drf_spectacular.utils import extend_schema_field


class CurrentUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'password']


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'github', 'image', 'first_name',
                  'last_name', 'email', 'username', 'groups']


class PostSerializer(ModelSerializer):
    owner = AuthorSerializer(read_only=True)
    # source = hyperlinked_identity_field(view_name='post-detail')

    class Meta:
        model = Post
        fields = ['id', 'title', 'source', 'origin', 'description', 'contentType', 'visibility', 'unlisted',
                  'content', 'published', 'owner', 'categories', 'image_link', 'image']
        read_only_fields = ['owner', 'count', ]
        ordering = ['-id']


class CommentSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'parentPost',  'comment',
                  'contentType', 'published']
        read_only_fields = ['author', 'parentPost']
        ordering = ['-id']


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ['from_author', 'to_author', 'status']


class FriendRequestSerializer(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_author', 'to_author', 'status']


class PostLikeSerializer(ModelSerializer):
    
    class Meta:
        model = PostLike
        fields = ['published', 'author', 'post', 'id']
        read_only_fields = ['author', 'post', 'id']
        ordering = ['-id']


class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['published', 'author', 'comment', 'id']
        ordering = ['-id']
        read_only_fields = ['author', 'comment', 'id']


class ConnectedNodeSerializer(ModelSerializer):
    class Meta:
        model = ConnectedNode
        fields = ['id', 'url', 'host', 'teamName']
