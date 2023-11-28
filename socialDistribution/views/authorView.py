from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from socialDistribution.pagination import Pagination, JsonObjectPaginator
from socialDistribution.serializers import AuthorSerializer
from ..models import Author
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from socialDistribution.util import team1, team2, secondInstance
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
            remote_authors = team1.get("authors/")
            for author in remote_authors.json()["items"]:
                all_authors.append(serializeTeam1Author(author))
            
            remote_authors1 = secondInstance.get("authors/")
            for author in remote_authors1.json()["results"]:
                # author["github"] = ""
                all_authors.append(AuthorSerializer(author).data)
        page = self.paginate_queryset(all_authors)
        return self.get_paginated_response(page)


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
                # remote_author = team1.get(f"authors/{author_pk}")
                # if remote_author.status_code == 200:
                #         author = remote_author.json()
                #         return Response(serializeTeam1Author(author))
                remote_author1 = secondInstance.get("authors/")
                if remote_author1.status_code == 200:
                    return Response(AuthorSerializer(remote_author1).data)

            # remote_author1 = team2.get(f"authors/{author_pk}/")
            # if remote_author1.status_code == 200:
            #     author = remote_author1.json()
            #     author["github"] = ""
            #     return Response(serializeTeam1Author(author))
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
