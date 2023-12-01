from rest_framework.response import Response
from socialDistribution.models import Author
from socialDistribution.serializers import PostSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from ..util import sendToEveryonesInbox, sendToFriendsInbox
from drf_spectacular.utils import extend_schema
from ..pagination import JsonObjectPaginator
from ..models import Post


class ShareView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        tags=['Share'],
        description='[local] share a post to AUTHOR_ID’s friends inbox'
    )
    def post(self, request, post_pk, format=None):
        # As an author, I can share other author’s public posts
        # As an author, I can re-share other author’s friend posts to my friends
        try:
            author = Author.objects.get(pk=request.user.id, type="author")
            post = Post.objects.get(pk=post_pk)
            if post.visibility == "FRIENDS":
                sendToFriendsInbox(author, PostSerializer(post).data)
            elif post.visibility == "PUBLIC": # TODO: check if all users get that post in their inbox
                sendToEveryonesInbox(PostSerializer(post).data)
            return Response({'message': 'Post shared'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
