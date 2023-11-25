from rest_framework import permissions
from rest_framework.response import Response
from socialDistribution.models import Author, Comment, Post
from socialDistribution.pagination import Pagination, JsonObjectPaginator
from socialDistribution.serializers import CommentSerializer
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from ..util import addToInbox
from socialDistribution.util import isFrontendRequest, team1, serializeTeam1Author, team2
import json

from rest_framework.renderers import JSONRenderer


class CommentViewSet(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = JsonObjectPaginator

    @extend_schema(
        tags=['Comments'],
        description='GET [local, remote] get the list of comments of the post whose id is POST_ID (paginated)'
    )
    def get(self, request, author_pk, post_pk, format=None):
        comments = Comment.objects.filter(post=post_pk)
        all_comments = json.loads(JSONRenderer().render(CommentSerializer(comments, many=True).data).decode('utf-8'))
        if isFrontendRequest(request):
            team1_comments = team1.get(f"authors/{author_pk}/posts/{post_pk}/comments")
            if team1_comments.status_code == 200:
                for comment in team1_comments.json()["comments"]:
                    all_comments.append({
                        "id": comment["id"],
                        "author": serializeTeam1Author(comment["author"]),
                        "comment": comment["comment"],
                        "contentType": comment["contentType"],
                        "published": comment["published"],
                        # "post": comment["post"],
                    })
            # team2_comments = team2.get(f"authors/{author_pk}/posts/{post_pk}/comments")
            # if team2_comments.status_code == 200:
            #     for comment in team2_comments.json()["comments"]:
            #         all_comments.append({
            #             "id": comment["id"],
            #             "author": serializeTeam1Author(comment["author"]),
            #             "comment": comment["comment"],
            #             "contentType": comment["contentType"],
            #             "published": comment["published"],
            #             # "post": comment["post"],
            #         })
        page = self.paginate_queryset(all_comments)
        return self.get_paginated_response(page)

    @extend_schema(
        tags=['Comments'],
    )
    def post(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author, post=post)

            # add the comment to post owners inbox
            addToInbox(post.author, serializer.data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
