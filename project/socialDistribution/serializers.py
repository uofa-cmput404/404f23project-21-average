from rest_framework import serializers
from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'url', 'github', 'user',
                  'profileImage', 'type', 'public']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'type', 'title', 'source', 'origin', 'description', 'contentType',
                  'content', 'published', 'owner', 'categories', 'count']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'commenter', 'parentPost', 'type', 'comment',
                  'contentType', 'published']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['from_author', 'to_author', 'status']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_author', 'to_author', 'status']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'author', 'post', 'type', 'published']


class ConnectedNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedNode
        fields = ['id', 'url', 'host', 'teamName']
