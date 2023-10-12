from rest_framework import serializers
from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'url', 'github']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['commenter', 'parentPost', 'type', 'comment',
                  'contentType', 'published']


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
