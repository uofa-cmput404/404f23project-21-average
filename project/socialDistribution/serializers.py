from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Post
from drf_spectacular.utils import extend_schema_field


class AuthorSerializer(ModelSerializer):
    # url = HyperlinkedIdentityField(
    #     view_name='authors-list', lookup_field='id')

    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'github', 'image', 'first_name',
                  'last_name', 'email', 'username', 'password', 'groups']


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'source', 'origin', 'description', 'contentType', 'visibility', 'unlisted',
                  'content', 'published', 'owner', 'categories', 'image_link', 'image']
        read_only_fields = ['owner', 'count', ]
        ordering = ['-id']


class CommentSerializer(ModelSerializer):

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

    class Meta:
        model = Like
        fields = ['id', 'author', 'post',  'published']
        ordering = ['-id']


class ConnectedNodeSerializer(ModelSerializer):
    class Meta:
        model = ConnectedNode
        fields = ['id', 'url', 'host', 'teamName']
