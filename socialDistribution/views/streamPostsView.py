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
from socialDistribution.util import sendToFriendsInbox, isFriend, serializeTeam1Author
import base64
from io import BytesIO
from PIL import Image
from django.http import HttpResponse
from ..util import isFrontendRequest, team1, team2, team3, serializeTeam1Post, sendToEveryonesInbox, serializeTeam3Post, serializeTeam2Post
import json
import uuid
from rest_framework.renderers import JSONRenderer


def getPostsFromAuthors():
    res = []
    team1Authors = team1.get("authors/")
    if team1Authors.status_code == 200:
        for author in team1Authors.json()["items"]:
            author1 = serializeTeam1Author(author)
            team1Posts = team1.get(f"authors/{author1['id']}/posts/")
            if team1Posts.status_code == 200:
                for post in team1Posts.json()["items"]:
                    res.append(serializeTeam1Post(post))

    team2Authors = team2.get("authors/")
    # TODO: fix this
    if team2Authors.status_code == 200:
        for author in team2Authors.json()["items"]:
            author2 = serializeTeam1Author(author)
            team2Posts = team2.get(f"authors/{author2['id'].split('/')[-1]}/posts")
            print(team2Posts.json())
            if team2Posts.status_code == 200:
                for post in team2Posts.json()["items"]:
                    # print(post)
                    res.append(serializeTeam3Post(post))

    team3Authors = team3.get("authors/")
    if team3Authors.status_code == 200:
        for author in team3Authors.json()["items"]:
            author3 = serializeTeam1Author(author)
            team3Posts = team3.get(f"authors/{author3['id'].split('/')[-1]}/posts/")
            if team3Posts.status_code == 200:
                for post in team3Posts.json()["items"]:
                    res.append(serializeTeam3Post(post))
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
        authorFriends = [(Author.objects.get(pk=friend["following"]["id"].split('/')[-1])) for friend in authorFriends]
        friendsPosts = Post.objects.filter(author__in=authorFriends, visibility="FRIENDS")

        all_posts = json.loads(JSONRenderer().render(PostSerializer(authorPosts, many=True).data + 
        PostSerializer(publicPosts, many=True).data + 
        PostSerializer(friendsPosts, many=True).data).decode('utf-8'))

        # get posts from other servers
        if isFrontendRequest(request):
            all_posts += getPostsFromAuthors()

        # add source to posts and return everything
        for post in all_posts:
            post["source"] = f"{settings.BASEHOST}/authors/{post['author']['id'].split('/')[-1]}/posts/{post['id'].split('/')[-1]}"
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
        # allComments = []

        if post.visibility == "PUBLIC":
            comments = Comment.objects.filter(post=post_pk)
        elif post.visibility == "FRIENDS" and isFriend(author, post.author):
            comments = Comment.objects.filter(post=post_pk, type="comment")

        # if isFrontendRequest(request):
        # TODO: check duplicate comment returns 
        allComments = json.loads(JSONRenderer().render(CommentSerializer(comments, many=True).data).decode('utf-8'))
        team1Comments = team1.get(f"authors/{author_pk}/posts/{post_pk}/comments")
        if team1Comments.status_code == 200:
            for comment in team1Comments.json()["comments"]:
                allComments.append({
                    "id": comment["id"],
                    "author": serializeTeam1Author(comment["author"]),
                    "comment": comment["comment"],
                    "contentType": comment["contentType"],
                    "published": comment["published"],
                    "type": "NodeComment",
                    "post": post_pk,
                })
        team2Comments = team2.get(f"authors/{author_pk}/posts/{post_pk}/comments")
        if team2Comments.status_code == 200:
            for comment in team2Comments.json()["comments"]:
                allComments.append({
                    "id": comment["id"],
                    "author": serializeTeam1Author(comment["author"]),
                    "comment": comment["comment"],
                    "contentType": comment["contentType"],
                    "published": comment["published"],
                    "type": "NodeComment",
                    "post": post_pk,
                })
        # team2_comments = team3.get(f"authors/{author_pk}/posts/{post_pk}/comments")
        # if team2_comments.status_code == 200:
        #     for comment in team2_comments.json()["comments"]:
        #         allComments.append({
        #             "id": comment["id"],
        #             "author": serializeTeam1Author(comment["author"]),
        #             "comment": comment["comment"],
        #             "contentType": comment["contentType"],
        #             "published": comment["published"],
        #             # "post": comment["post"],
        #         })
        
