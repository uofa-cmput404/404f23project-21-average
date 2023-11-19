from requests import Response
from socialDistribution.models import ConnectedNode, Follow, FriendRequest
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import ConnectedNodeSerializer, FollowSerializer, FriendRequestSerializer
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
        follows = Follow.objects.filter(from_author=author_pk)
        page = self.paginate_queryset(follows)
        return self.get_paginated_response(FollowSerializer(page, many=True).data)

class FollowDeatilViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination
    
    @extend_schema(
        tags=['Followers'],
        description='check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID'
    )
    def get(self, request, author_pk, format=None):
        follows = Follow.objects.filter(from_author=author_pk)
        page = self.paginate_queryset(follows)
        return self.get_paginated_response(FollowSerializer(page, many=True).data)
    
    @extend_schema(
        tags=['Followers'],
        description='Remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID'
    )
    def delete(self, request, author_pk, format=None):
        follows = Follow.objects.filter(from_author=author_pk)
        page = self.paginate_queryset(follows)
        return self.get_paginated_response(FollowSerializer(page, many=True).data)
    
    @extend_schema(
        tags=['Followers'],
        description='Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)'
    )
    def put(self, request, author_pk, format=None):
        follows = Follow.objects.filter(from_author=author_pk)
        page = self.paginate_queryset(follows)
        return self.get_paginated_response(FollowSerializer(page, many=True).data)


class FriendRequestViewSet(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, author_pk, format=None):
        friend_requests = FriendRequest.objects.filter(to_author=author_pk)
        page = self.paginate_queryset(friend_requests)
        return self.get_paginated_response(FriendRequestSerializer(page, many=True).data)
    
    def post(self, request, author_pk, format=None):
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            friend_request = serializer.save(to_author=author_pk)
            return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConnectedNodeViewSet(generics.ListCreateAPIView):
    queryset = ConnectedNode.objects.all()
    serializer_class = ConnectedNodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination