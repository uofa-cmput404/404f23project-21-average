from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from socialDistribution.pagination import Pagination, JsonObjectPaginator
from socialDistribution.serializers import AuthorSerializer
from ..models import Author
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from socialDistribution.util import team1, team3, team2
import json
from rest_framework.renderers import JSONRenderer
from ..util import isFrontendRequest, serializeTeam1Author
from rest_framework import status


class AuthorListViewSet(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = JsonObjectPaginator
    
    @extend_schema(
        tags=['Authors'],
        description='Get the list of authors'
    )
    def get(self, request, *args, **kwargs):
        authors = Author.objects.filter(type="author").all()

        # check request origin
        all_authors = json.loads(JSONRenderer().render(AuthorSerializer(authors, many=True).data).decode('utf-8'))
        if isFrontendRequest(request):
            team1RemoteAuthors = team1.get("authors/")
            for author in team1RemoteAuthors.json()["items"]:
                all_authors.append(serializeTeam1Author(author))
            
            team2RemoteAuthors = team2.get("authors/")
            for author in team2RemoteAuthors.json()["items"]:
                all_authors.append(serializeTeam1Author(author))

            team3RemoteAuthors = team3.get("authors/")
            for author in team3RemoteAuthors.json()["items"]:
                all_authors.append(serializeTeam1Author(author))

        page = self.paginate_queryset(all_authors)
        return self.get_paginated_response(page)


class AuthorDetailView(APIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @extend_schema(
        tags=['Authors'],
    )
    def get(self, request, author_pk, format=None):
        try:
            author = Author.objects.get(pk=author_pk)
        except:
            if isFrontendRequest(request):
                team1RemoteAuthor = team1.get(f"authors/{author_pk}")
                if team1RemoteAuthor.status_code == 200:
                    author = team1RemoteAuthor.json()
                    return Response(serializeTeam1Author(author))
                
                team2RemoteAuthor = team2.get(f"authors/{author_pk}")
                if team2RemoteAuthor.status_code == 200:
                    author = team2RemoteAuthor.json()
                    return Response(serializeTeam1Author(author))

                team3RemoteAuthor = team3.get(f"authors/{author_pk}")
                if team3RemoteAuthor.status_code == 200:
                    author = team3RemoteAuthor.json()
                    return Response(serializeTeam1Author(author))
                
            return Response({'message': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    @extend_schema(
        tags=['Authors'],
    )
    def post(self, request, author_pk, format=None):
        author = get_object_or_404(Author, pk=author_pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @extend_schema(
        tags=['Authors'],
        description='Delete author'
    )
    def delete(self, request, author_pk, *args, **kwargs):
        author = Author.objects.get(pk=author_pk)
        print(author.id)
        # delete the author from the database
        author.delete()
        return Response(status=204)


class NodeListViewSet(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = JsonObjectPaginator
    paginate_by_param = 'page_size'
    
    @extend_schema(
        tags=['Authors'],
        description='Get the list of connected nodes'
    )
    def get(self, request, *args, **kwargs):
        authors = Author.objects.filter(type="node").all()
        # check request origin
        all_authors = json.loads(JSONRenderer().render(AuthorSerializer(authors, many=True).data).decode('utf-8'))
        
        page = self.paginate_queryset(all_authors)
        return self.get_paginated_response(page)
