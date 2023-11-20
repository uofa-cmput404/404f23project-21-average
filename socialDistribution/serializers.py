from rest_framework.serializers import ModelSerializer
from .models import *
from .models import Author, Post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Post, Inbox
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
    class Meta:
        model = Post
        fields = ['id', 'title', 'source', 'origin', 'description', 'contentType', 'visibility', 'unlisted',
                  'content', 'published', 'owner', 'categories', 'image_link', 'image', 'imageOnlyPost', 'count']
        read_only_fields = ['owner', 'count', 'published', 'id']
        ordering = ['-id']


class CommentSerializer(ModelSerializer):
    author = AuthorSerializer()
    class Meta:
        model = Comment
        fields = ['id', 'author', 'parentPost',  'comment',
                  'contentType', 'published']
        read_only_fields = ['parentPost', 'published', 'id']
        ordering = ['-id']


class FollowSerializer(ModelSerializer):
    from_author = AuthorSerializer(read_only=True)
    to_author = AuthorSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = ['from_author', 'to_author']
        read_only_fields = ['from_author', 'to_author']


class FriendRequestSerializer(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = [ 'from_author', 'to_author', 'status']
        read_only_fields = ['from_author', 'to_author', 'status']


class PostLikeSerializer(ModelSerializer):
    
    class Meta:
        model = PostLike
        fields = ['published', 'author', 'post', 'id']
        read_only_fields = ['author', 'post', 'id', 'published']
        ordering = ['-id']


class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['published', 'author', 'comment', 'id']
        ordering = ['-id']
        read_only_fields = ['author', 'comment', 'id', 'published']


class ConnectedNodeSerializer(ModelSerializer):
    class Meta:
        model = ConnectedNode
        fields = ['id', 'url', 'host', 'teamName']

#Added Model Serializer of Inbox
class InboxSerializer(ModelSerializer):
    class Meta:
        model = Inbox
        fields = '__all__'
