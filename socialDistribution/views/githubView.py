import requests
from socialDistribution.models import Author
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework import permissions


class GitHubView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """
    GitHubView handles the GitHub OAuth2 login and callback.
    """
    @extend_schema(
        tags=['GitHub'],
        description='[local] get a list of GitHub events for AUTHOR_ID (paginated)'
    )
    def get(self, request, author_pk, format=None):
        """_summary_

        Args:
            request (_type_): _description_
            author_pk (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        author = Author.objects.get(pk=author_pk)
        githubData = requests.get('https://api.github.com/users/'+ author.github.split('/')[-1]+'/events')
        
        return Response(githubData, status=status.HTTP_200_OK)
        