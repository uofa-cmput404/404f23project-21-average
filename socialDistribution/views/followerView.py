

from socialDistribution import permissions
from socialDistribution.models import ConnectedNode, Follow, FriendRequest
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import ConnectedNodeSerializer, FollowSerializer, FriendRequestSerializer
from rest_framework import generics


class FollowViewSet(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination


class FriendRequestViewSet(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ConnectedNodeViewSet(generics.ListCreateAPIView):
    queryset = ConnectedNode.objects.all()
    serializer_class = ConnectedNodeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination