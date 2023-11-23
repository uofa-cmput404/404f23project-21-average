from rest_framework.serializers import ModelSerializer
from .models import Post, Comment, Follow, PostLike, CommentLike, ConnectedNode, Inbox, Author


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'github', 'image', 'first_name',
                  'last_name', 'email', 'username', 'type']


class PostSerializer(ModelSerializer):
    owner = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'type', 'source', 'origin', 'description', 'contentType', 'visibility', 'unlisted',
                  'content', 'published', 'owner', 'categories', 'image_link', 'image', 'imageOnlyPost', 'count']
        read_only_fields = ['owner', 'count', 'published', 'id', 'origin', 'source', 'type']
        ordering = ['-id']


class CommentSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'parentPost', 'comment', 'type',
                  'contentType', 'published']
        read_only_fields = ['author', 'parentPost', 'published', 'id', 'type']
        ordering = ['-id']


class FollowSerializer(ModelSerializer):
    following = AuthorSerializer()
    follower = AuthorSerializer()

    class Meta:
        model = Follow
        fields = ['following', 'follower', 'status', 'id']
        read_only_fields = ['following', 'follower', 'id', 'status']


class PostLikeSerializer(ModelSerializer):
    
    class Meta:
        model = PostLike
        fields = ['published', 'author', 'post', 'id', 'type']
        read_only_fields = ['author', 'post', 'id', 'published', 'type']
        ordering = ['-id']


class CommentLikeSerializer(ModelSerializer):

    class Meta:
        model = CommentLike
        fields = ['published', 'author', 'comment', 'id', 'type']
        ordering = ['-id']
        read_only_fields = ['author', 'comment', 'id', 'published', 'type']


class ConnectedNodeSerializer(ModelSerializer):

    class Meta:
        model = ConnectedNode
        fields = ['id', 'url', 'teamName']


class InboxSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Inbox
        fields = ['id', 'author', 'items', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'author']

