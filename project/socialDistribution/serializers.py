from rest_framework.serializers import ModelSerializer
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
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'
        # fields = ['id', 'host', 'displayName', 'github', 'user',
        #           'image']


class PostSerializer(ModelSerializer):
    # parent_lookup_kwargs = {
    #     'author_pk': 'author___pk',
    # }

    class Meta:
        model = Post
        fields = ['id', 'title', 'source', 'origin', 'description', 'contentType', 'visibility', 'unlisted',
                  'content', 'published', 'owner', 'categories', 'image_link', 'image']
        read_only_fields = ['owner', 'count', ]
        ordering = ['-id']


class CommentSerializer(ModelSerializer):
    # parent_lookup_kwargs = {
    #     'post_pk': 'post__pk',
    #     'author_pk': 'author___pk',
    # }

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


# class LikeSerializer(ModelSerializer):
#     # parent_lookup_kwargs = {
#     #     'post_pk': 'post__pk',
#     #     'author_pk': 'author___pk',
#     # }

#     class Meta:
#         model = Like
#         fields = ['id', 'author', 'post',  'published']
#         ordering = ['-id']

class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['published']
        read_only_fields = ['author', 'post', 'id']
        ordering = ['-id']


class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['published']
        ordering = ['-id']
        read_only_fields = ['author', 'comment', 'id']


class ConnectedNodeSerializer(ModelSerializer):
    class Meta:
        model = ConnectedNode
        fields = ['id', 'url', 'host', 'teamName']
