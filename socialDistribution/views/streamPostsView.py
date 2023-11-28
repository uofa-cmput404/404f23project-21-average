import requests
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework import generics
from django.conf import settings
from drf_spectacular.utils import extend_schema
from socialDistribution.models import Author, Post, Comment
from socialDistribution.pagination import Pagination, JsonObjectPaginator
from socialDistribution.serializers import PostSerializer, FollowSerializer, AuthorSerializer, \
    CommentSerializer
from socialDistribution.util import sendToFriendsInbox, isFriend, serializeTeam1Author, secondInstance
import base64
from io import BytesIO
from PIL import Image
from django.http import HttpResponse
from ..util import isFrontendRequest, team1, team2, serializeTeam1Post, sendToEveryonesInbox
import json
from rest_framework.renderers import JSONRenderer


def getPostsFromAuthors():
    res = []
    remote_author1 = secondInstance.get("authors/")
    if remote_author1.status_code == 200:
        for author in remote_author1.json()["results"]:
            author1 = AuthorSerializer(author).data
            remote_posts = secondInstance.get(f"authors/{author1['id']}/posts/")
            if remote_posts.status_code == 200:
                for post in remote_posts.json()["results"]:
                    res.append(PostSerializer(post).data)
    team1_authors = team1.get("authors/")
    if team1_authors.status_code == 200:
        for author in team1_authors.json()["items"]:
            author1 = serializeTeam1Author(author)
            team1_posts = team1.get(f"authors/{author1['id']}/posts/")
            if team1_posts.status_code == 200:
                for post in team1_posts.json()["items"]:
                    res.append(serializeTeam1Post(post))
    # team2_posts = team2.get(f"authors/{author_pk}/posts/")
            # if team2_posts.status_code == 200:
            #     for post in team2_posts.json()["items"]:
            #         post["author"]["github"] = ""
            #         post["categories"] = ""
            #         all_posts.append(serializeTeam1Post(post))
    return res


class StreamPostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = JsonObjectPaginator

    @extend_schema(
        tags=['Posts'],
        # TODO: check if 'everyone' implies posts fromo other servers
        description='returns the all the posts that AUTHOOR_ID can see (paginated)\
            returns posts from author, their friends, and public posts'
    )
    def get(self, request, author_pk, format=None):
        author = Author.objects.get(pk=author_pk)

        # get posts from author, their friends, and public posts
        # TODO: check unlisted posts
        authorPosts = Post.objects.filter(author=author)
        publicPosts = Post.objects.filter(visibility="PUBLIC", unlisted=False)
        
        authorFriends = FollowSerializer(author.following.filter(status="Accepted"), many=True).data
        authorFriends = [(Author.objects.get(pk=friend["following"]["id"])) for friend in authorFriends]
        friendsPosts = Post.objects.filter(author__in=authorFriends, visibility="FRIENDS")

        all_posts = json.loads(JSONRenderer().render(PostSerializer(authorPosts, many=True).data + 
        PostSerializer(publicPosts, many=True).data + 
        PostSerializer(friendsPosts, many=True).data).decode('utf-8'))

        # get posts from other servers
        if isFrontendRequest(request):
            all_posts += getPostsFromAuthors()

        # add source to posts and return everything
        for post in all_posts:
            post["source"] = f"{settings.BASEHOST}/authors/{post['author']['id']}/posts/{post['id']}"
        page = self.paginate_queryset(all_posts)
        return self.get_paginated_response(page)


class StreamComments(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = JsonObjectPaginator

    @extend_schema(
        tags=['Comments'],
        description='returns all the comments that AUTHOR_ID can see (paginated)'
    )
    def get(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=request.user.id)
        post = Post.objects.get(pk=post_pk)
        all_comments = []

        if post.visibility == "PUBLIC":
            comments = Comment.objects.filter(post=post_pk)
        elif post.visibility == "FRIENDS" and isFriend(author, post.author):
            comments = Comment.objects.filter(post=post_pk, type="comment")

        # if isFrontendRequest(request):
        # TODO: check duplicate comment returns 
        all_comments = json.loads(JSONRenderer().render(CommentSerializer(comments, many=True).data).decode('utf-8'))
        team1_comments = team1.get(f"authors/{author_pk}/posts/{post_pk}/comments")
        if team1_comments.status_code == 200:
            for comment in team1_comments.json()["comments"]:
                all_comments.append({
                    "id": comment["id"],
                    "author": serializeTeam1Author(comment["author"]),
                    "comment": comment["comment"],
                    "contentType": comment["contentType"],
                    "published": comment["published"],
                    "type": "NodeComment",
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
        
