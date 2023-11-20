from rest_framework.response import Response
from socialDistribution.models import Author, ConnectedNode, FriendRequest
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import AuthorSerializer, ConnectedNodeSerializer, FriendRequestSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from drf_spectacular.utils import extend_schema


class FriendRequestDetailViewSet(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @extend_schema(
        tags=['Befriend'],
        description='Add FOREIGN_AUTHOR_ID as a friend of AUTHOR_ID (must be authenticated)'
    )
    def get(self, request, author_pk, foreign_author_pk, format=None):
        friend_requests = FriendRequest.objects.filter(to_author=author_pk)
        page = self.paginate_queryset(friend_requests)
        return self.get_paginated_response(FriendRequestSerializer(page, many=True).data)

    @extend_schema(
        tags=['Befriend'],
        description='Add FOREIGN_AUTHOR_ID as a friend of AUTHOR_ID (must be authenticated)'
    )
    def put(self, request, author_pk, foreign_author_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        foreign_author = Author.objects.get(pk=foreign_author_pk)
        # create follow object
        follow = FriendRequest.objects.filter(from_author=foreign_author, to_author=author)
        if follow:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        follow = FriendRequest.objects.create(from_author=foreign_author, to_author=author)
        return Response(FriendRequestSerializer(follow).data, status=status.HTTP_201_CREATED)


class FriendRequestListViewSet(generics.ListAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination
    
    @extend_schema(
        tags=['Befriend'],
        description='[local] get a list of friend requests for AUTHOR_ID (paginated)'
    )
    def get(self, request, author_pk, format=None):
        friend_requests = FriendRequest.objects.filter(to_author=author_pk)
        friends = Author.objects.filter(pk__in=friend_requests.values('from_author'))
        page = self.paginate_queryset(friends)
        return self.get_paginated_response(AuthorSerializer(page, many=True).data)


class ConnectedNodeViewSet(generics.ListCreateAPIView):
    queryset = ConnectedNode.objects.all()
    serializer_class = ConnectedNodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination