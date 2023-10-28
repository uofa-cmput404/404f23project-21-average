from rest_framework.serializers import ModelSerializer
from .models import *


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'github', 'user',
                  'profileImage',  'public', ]
        read_only_fields = ['user']


class PostSerializer(ModelSerializer):
    parent_lookup_kwargs = {
        'author_pk': 'author___pk',
    }

    class Meta:
        model = Post
        fields = ['id',  'title', 'source', 'origin', 'description', 'contentType',
                  'content', 'published', 'categories', 'count', 'owner', ]
        read_only_fields = ['owner', 'count', ]
        ordering = ['-id']

    def create(self, validated_data):
        author = self.context['request'].user.author
        post = Post.objects.create(owner=author, **validated_data)
        return post


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

    def create(self, validated_data):
        author = self.context['request'].user.author
        post = Post.objects.get(pk=self.context['view'].kwargs['post_pk'])
        comment = Comment.objects.create(
            commenter=author, parentPost=post, **validated_data)
        return comment


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
