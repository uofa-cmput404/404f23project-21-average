from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from socialDistribution.pagination import Pagination, JsonObjectPaginator
from socialDistribution.serializers import AuthorSerializer
from ..models import Author
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from socialDistribution.util import vibely, ctrlAltDelete, socialSync
import json
from rest_framework.renderers import JSONRenderer
from ..util import isFrontendRequest, serializeVibelyAuthor
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
            vibelyRemoteAuthors = vibely.get("authors/")
            if vibelyRemoteAuthors.status_code == 200:
                for author in vibelyRemoteAuthors.json()["items"]:
                    all_authors.append(serializeVibelyAuthor(author))
            
            socialSyncRemoteAuthors = socialSync.get("authors/")
            if socialSyncRemoteAuthors.status_code == 200:
                for author in socialSyncRemoteAuthors.json()["items"]:
                    all_authors.append(serializeVibelyAuthor(author))

            ctrlAltDeleteRemoteAuthors = ctrlAltDelete.get("authors/")
            print(ctrlAltDeleteRemoteAuthors.text)
            if ctrlAltDeleteRemoteAuthors.status_code == 200 and ctrlAltDeleteRemoteAuthors.text != "error\n":
                for author in ctrlAltDeleteRemoteAuthors.json()["items"] :
                    all_authors.append(serializeVibelyAuthor(author))

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
                vibelyRemoteAuthor = vibely.get(f"authors/{author_pk}")
                if vibelyRemoteAuthor.status_code == 200:
                    author = vibelyRemoteAuthor.json()
                    return Response(serializeVibelyAuthor(author))
                
                socialSyncRemoteAuthor = socialSync.get(f"authors/{author_pk}")
                if socialSyncRemoteAuthor.status_code == 200:
                    author = socialSyncRemoteAuthor.json()
                    return Response(serializeVibelyAuthor(author))

                ctrlAltDeleteRemoteAuthor = ctrlAltDelete.get(f"authors/{author_pk}")
                if ctrlAltDeleteRemoteAuthor.status_code == 200:
                    author = ctrlAltDeleteRemoteAuthor.json()
                    return Response(serializeVibelyAuthor(author))
                
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
