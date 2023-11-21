from socialDistribution.models import ConnectedNode
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import ConnectedNodeSerializer
from rest_framework import generics
from rest_framework import permissions


class ConnectedNodeViewSet(generics.ListCreateAPIView):
    queryset = ConnectedNode.objects.all()
    serializer_class = ConnectedNodeSerializer
    permission_classes = []
    pagination_class = Pagination
    