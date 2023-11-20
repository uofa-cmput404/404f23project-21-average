from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import AuthorSerializer
from ..models import *
from rest_framework import generics
from drf_spectacular.utils import extend_schema


class AuthorListViewSet(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination
    paginate_by_param = 'page_size'
    
    @extend_schema(
        tags=['Authors'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AuthorDetailView(APIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    @extend_schema(
        tags=['Authors'],
    )
    def get(self, request, author_pk, format=None):
        author = get_object_or_404(Author, pk=author_pk)
        serializer_context = {
            'request': request,
        }
        serializer = AuthorSerializer(author, context=serializer_context)
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
