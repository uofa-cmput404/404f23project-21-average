from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Post
from drf_spectacular.utils import extend_schema_field


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'github', 'user',
                  'profileImage']


# @extend_schema_field({'type': "string", 'format': 'binary',
#                       'example': {
#                           "image": {"url": "string", "name": "string"},
#                           "thumbnail": {"url": "string", "name": "string"}
#                       }
#                       })
class PostSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'author_pk': 'author___pk',
    }

    class Meta:
        model = Post
        fields = ['id', 'title', 'source', 'origin', 'description', 'contentType', 'visibility', 'unlisted',
                  'content', 'published', 'owner', 'categories', 'image_link', 'image']
        read_only_fields = ['owner', 'count', ]
        ordering = ['-id']


class CommentSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'post_pk': 'post__pk',
        'author_pk': 'author___pk',
    }

    class Meta:
        model = Comment
        fields = ['id', 'commenter', 'parentPost',  'comment',
                  'contentType', 'published']
        read_only_fields = ['commenter', 'parentPost']
        ordering = ['-id']


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = ['from_author', 'to_author', 'status']


class FriendRequestSerializer(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_author', 'to_author', 'status']


class LikeSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'post_pk': 'post__pk',
        'author_pk': 'author___pk',
    }

    class Meta:
        model = Like
        fields = ['id', 'author', 'post',  'published']
        ordering = ['-id']


class ConnectedNodeSerializer(ModelSerializer):
    class Meta:
        model = ConnectedNode
        fields = ['id', 'url', 'host', 'teamName']
