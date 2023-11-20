from rest_framework.response import Response
from socialDistribution.models import Author, ConnectedNode, Follow, FriendRequest
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import AuthorSerializer, ConnectedNodeSerializer, FollowSerializer, FriendRequestSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from drf_spectacular.utils import extend_schema


class FollowViewSet(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination
    
    @extend_schema(
        tags=['Followers'],
        description='[local, remote] get a list of authors who are AUTHOR_ID’s followers'
    )
    def get(self, request, author_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        follows = Follow.objects.filter(to_author=author)
        followers = Author.objects.filter(pk__in=follows.values('from_author'))
        
        page = self.paginate_queryset(followers)
        return self.get_paginated_response(AuthorSerializer(page, many=True).data)


class FollowDetailViewSet(generics.GenericAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination
    
    @extend_schema(
        tags=['Followers'],
        description='check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID'
    )
    def get(self, request, author_pk, foreign_author_pk, format=None):
        # return true if foreign_author is a follower of author
        author = Author.objects.get(pk=author_pk)
        foreign_author = Author.objects.get(pk=foreign_author_pk)
        follow = Follow.objects.filter(from_author=foreign_author, to_author=author)
        if follow:
            return Response(True)
        return Response(False)
    
    @extend_schema(
        tags=['Followers'],
        description='Remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID'
    )
    def delete(self, request, author_pk, foreign_author_pk, format=None):
        
        author = Author.objects.get(pk=author_pk)
        foreign_author = Author.objects.get(pk=foreign_author_pk)
        # create follow object
        follow = Follow.objects.filter(from_author=foreign_author, to_author=author)
        
        if follow:
            follow.delete()
            return Response({'message': 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        
    
    @extend_schema(
        tags=['Followers'],
        description='Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)'
    )
    def put(self, request, author_pk, foreign_author_pk, format=None):
        print(request, request.data)
        author = Author.objects.get(pk=author_pk)
        foreign_author = Author.objects.get(pk=foreign_author_pk)
        
        if author == foreign_author:
            return Response({'message': 'cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Follow.objects.filter(from_author=foreign_author, to_author=author):
            return Response({'message': 'already following'}, status=status.HTTP_400_BAD_REQUEST)
        
        Follow.objects.create(from_author=foreign_author, to_author=author)
        return Response({'message': 'Followed Successfully'}, status=status.HTTP_201_CREATED)
