from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Post
from drf_spectacular.utils import extend_schema_field


# class RegistrationSerializer(RegisterSerializer):
#     class Meta:
#         model: User
#         fields = ['id', 'username', 'email',
#                   'password', 'first_name', 'last_name']

#     def save(self, request):
#         user = super().save(request)
#         user.is_active = False
#         user.save()
#         return user

class CurrentUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'password']


class AuthorSerializer(ModelSerializer):
    # url = HyperlinkedIdentityField(
    #     view_name='authors-list', lookup_field='id')

    class Meta:
        model = Author
        fields = ['id', 'host', 'displayName', 'github', 'image', 'first_name',
                  'last_name', 'email', 'username', 'groups']


class PostSerializer(ModelSerializer):
    owner = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'source', 'origin', 'description', 'contentType', 'visibility', 'unlisted',
                  'content', 'published', 'owner', 'categories', 'image_link', 'image']
        read_only_fields = ['owner', 'count', ]
        ordering = ['-id']


class CommentSerializer(ModelSerializer):
    commenter = AuthorSerializer(read_only=True)

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


class PostLikeSerializer(ModelSerializer):
    
    class Meta:
        model = PostLike
        fields = ['published', 'author', 'post', 'id']
        read_only_fields = ['author', 'post', 'id']
        ordering = ['-id']


class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['published', 'author', 'comment', 'id']
        ordering = ['-id']
        read_only_fields = ['author', 'comment', 'id']


class ConnectedNodeSerializer(ModelSerializer):
    class Meta:
        model = ConnectedNode
        fields = ['id', 'url', 'host', 'teamName']
