from rest_framework.serializers import ModelSerializer
from .models import Post, Comment, Follow, PostLike, CommentLike, Inbox, Author
from rest_framework import serializers
from django.conf import settings


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'github', 'image', 'first_name',
                  'last_name', 'email', 'username', 'type']


class PostSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)
    categories = serializers.SerializerMethodField(method_name='get_categories')
    # image = serializers.SerializerMethodField(method_name='get_image_link')

    class Meta:
        model = Post
        fields = ['id', 'title', 'type', 'source', 'origin', 'description', 'contentType', 'visibility', 'unlisted',
                  'content', 'published', 'author', 'categories', 'image_link', 'image', 'imageOnlyPost', 'count']
        read_only_fields = ['author', 'count', 'published', 'id', 'origin', 'source', 'type']
        ordering = ['-id']

    def get_categories(self, obj):
        # if obj.categories is None:
        #     return []
        try:
            return obj.categories.split(",")
        except:
            return []
    
    # def get_image_link(self, obj):
    #     if obj.image:
    #         return settings.BASEHOST[0:-4] + obj.image.url
    #     return None


class CommentSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'comment', 'type',
                  'contentType', 'published']
        read_only_fields = ['author', 'post', 'published', 'id', 'type']
        ordering = ['-id']


class FollowSerializer(ModelSerializer):
    following = AuthorSerializer(read_only=True)
    follower = AuthorSerializer(read_only=True)
    summary = serializers.SerializerMethodField(method_name='get_summary')

    class Meta:
        model = Follow
        fields = ['following', 'follower', 'status', 'id', 'summary']
        read_only_fields = ['following', 'follower', 'id', 'status', 'summary']
    
    def get_summary(self, obj):
        if obj.summary:
            return obj.summary
        return f"{obj.follower.displayName} wants to follow {obj.following.displayName}"


class PostLikeSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)
    object = serializers.SerializerMethodField(method_name='get_object')
    
    class Meta:
        model = PostLike
        fields = ['published', 'author', 'post', 'id', 'type', 'summary', 'context', 'object']
        read_only_fields = ['author', 'post', 'id', 'published', 'type', 'summary', 'context', 'object']
        ordering = ['-id']
    
    def get_object(self, obj):
        if obj.post:
            return f"{settings.BASEHOST}/authors/{obj.author.id}/posts/{obj.post.id}"
        else:
            return obj.object


class CommentLikeSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)
    object = serializers.SerializerMethodField(method_name='get_object')

    class Meta:
        model = CommentLike
        fields = ['published', 'author', 'comment', 'id', 'type', 'summary', 'context', 'object']
        ordering = ['-id']
        read_only_fields = ['author', 'comment', 'id', 'published', 'type', 'summary', 'context', 'object']

    def get_object(self, obj):
        if obj.comment:
            return f"{settings.BASEHOST}/authors/{obj.author.id}/posts/{obj.comment.post.id}/comments/{obj.comment.id}"
        else:
            return obj.object


class InboxSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)
    items = serializers.JSONField()

    class Meta:
        model = Inbox
        fields = ['id', 'author', 'items', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'author']

