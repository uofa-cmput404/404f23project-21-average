from rest_framework import serializers
from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'url', 'github', 'bio']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'source', 'origin', 'description', 'contentType', 'content',
                  'author', 'categories', 'count', 'published', 'visibility', 'visibleTo', 'unlisted']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'posts', 'comment',
                  'contentType', 'published', 'id']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['from_author', 'to_author', 'status', 'id']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['from_author', 'to_author', 'status', 'id']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['author', 'posts', 'type', 'published', 'id']


class ConnectedNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedNode
        fields = ['id', 'url', 'host', 'teamName']