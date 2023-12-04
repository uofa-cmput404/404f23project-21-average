import requests
from socialDistribution.models import Author
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework import generics
import json


class GitHubView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    """
    GitHubView handles the GitHub OAuth2 login and callback.
    """

    @extend_schema(
        tags=['GitHub'],
        description='[local] get a list of GitHub events for AUTHOR_ID (paginated)'
    )
    def post(self, request, author_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        try:
            githubData = requests.get('https://api.github.com/users/' + author.github.split('/')[-1] + '/events')
            githubJSON = json.loads(githubData.text)
            return Response(githubJSON, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'GitHub not found'}, status=status.HTTP_404_NOT_FOUND)
        
