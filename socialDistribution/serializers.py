from rest_framework.serializers import ModelSerializer
from .models import *
from .models import Author, Post
from .models import Author, Post, Inbox


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
        read_only_fields = ['owner', 'count', 'published', 'id', 'origin', 'source']
        ordering = ['-id']


class CommentSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'author', 'parentPost',  'comment',
                  'contentType', 'published']
        read_only_fields = ['author', 'parentPost', 'published', 'id']
        ordering = ['-id']


class FollowSerializer(ModelSerializer):
    from_author = AuthorSerializer(read_only=True)
    to_author = AuthorSerializer(read_only=True)
    class Meta:
        model = Follow
        fields = ['from_author', 'to_author']
        read_only_fields = ['from_author', 'to_author']


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
        fields = ['id', 'url', 'teamName']

#Added Model Serializer of Inbox
class InboxSerializer(ModelSerializer):
    class Meta:
        model = Inbox
        fields = ['id', 'type', 'sender', 'recipient', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'recipient']
