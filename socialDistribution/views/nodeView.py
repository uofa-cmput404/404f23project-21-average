from socialDistribution.models import ConnectedNode, Author
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import ConnectedNodeSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
import base64
from django.contrib.auth.hashers import make_password


class ConnectedNodeViewSet(generics.GenericAPIView):
    queryset = ConnectedNode.objects.all()
    serializer_class = ConnectedNodeSerializer
    permission_classes = []
    pagination_class = Pagination

    def post(self, request, format=None):
        serializer = ConnectedNodeSerializer(data=request.data)
        node = Author.objects.create(type="node", username=request.data['teamName'], host=request.data['url'],
        is_active=True, is_staff=True, is_superuser=False, password=make_password(request.data['url']))
        # node.set_password(node.cleaned_data['password'])
        node.save()
        if serializer.is_valid():
            serializer.save(api_user=node)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    

class ConnectedNodeTokenView(generics.GenericAPIView):
    queryset = ConnectedNode.objects.all()
    serializer_class = ConnectedNodeSerializer
    permission_classes = []
    pagination_class = Pagination
    
    def post(self, request, format=None):
        teamName = request.data['teamName']
        url = request.data['url']
        node = ConnectedNode.objects.get(teamName=teamName, url=url)
        api_user = node.api_user
        token = api_user.username + ":" + api_user.password
        token_bytes = token.encode('utf-8')
        print(api_user.username, api_user.password)
        return Response({'Basic Token': base64.b64encode(token_bytes)}, status=status.HTTP_200_OK)
