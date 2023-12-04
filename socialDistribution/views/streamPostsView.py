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
from socialDistribution.pagination import  JsonObjectPaginator
from socialDistribution.serializers import PostSerializer, FollowSerializer, CommentSerializer
from socialDistribution.util import isFriend, serializeVibelyAuthor
from ..util import isFrontendRequest, vibely, socialSync, serializeVibelyPost, serializeCtrlAltDeletePost, getUUID
import json
from rest_framework.renderers import JSONRenderer


def getPostsFromAuthors():
    res = []
    vibelyAuthors = vibely.get("authors/")
    if vibelyAuthors.status_code == 200:
        for author in vibelyAuthors.json()["items"]:
            author1 = serializeVibelyAuthor(author)
            vibelyPosts = vibely.get(f"authors/{getUUID(author1['id'])}/posts/")
            print(vibelyPosts)
            if vibelyPosts.status_code == 200:
                for post in vibelyPosts.json()["items"]:
                    res.append(serializeVibelyPost(post))

    socialSyncAuthors = socialSync.get("authors/")
    if socialSyncAuthors.status_code == 200:
        for author in socialSyncAuthors.json()["items"]:
            author2 = serializeVibelyAuthor(author)
            socialSyncPosts = socialSync.get(f"authors/{getUUID(author2['id'])}/posts")
            print(socialSyncPosts)
            if socialSyncPosts.status_code == 200:
                for post in socialSyncPosts.json()["items"]:
                    res.append(serializeCtrlAltDeletePost(post))

    # ctrlAltDeleteAuthors = ctrlAltDelete.get("authors/")
    # if ctrlAltDeleteAuthors.status_code == 200:
    #     for author in ctrlAltDeleteAuthors.json()["items"]:
    #         author3 = serializeVibelyAuthor(author)
    #         print(author3)
    #         ctrlAltDeletePosts = ctrlAltDelete.get(f"authors/{getUUID(author3['id'])}/posts/")
    #         print(ctrlAltDeletePosts.url)
    #         print(ctrlAltDeletePosts.text, ctrlAltDeletePosts.status_code, ctrlAltDeletePosts.url)
    #         if ctrlAltDeletePosts.status_code == 200:
    #             for post in ctrlAltDeletePosts.json()["items"]:
    #                 res.append(serializeCtrlAltDeletePost(post))
    return res


class StreamPostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = JsonObjectPaginator

    @extend_schema(
        tags=['Posts'],
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
        authorFriends = [(Author.objects.get(pk=getUUID(friend["following"]["id"]))) for friend in authorFriends]
        friendsPosts = Post.objects.filter(author__in=authorFriends, visibility="FRIENDS")

        all_posts = json.loads(JSONRenderer().render(PostSerializer(authorPosts, many=True).data + 
        PostSerializer(publicPosts, many=True).data + 
        PostSerializer(friendsPosts, many=True).data).decode('utf-8'))

        # get posts from other servers
        if isFrontendRequest(request):
            all_posts += getPostsFromAuthors()

        # add source to posts and return everything
        for post in all_posts:
            post["source"] = f"{settings.BASEHOST}/authors/{getUUID(post['author']['id'])}/posts/{getUUID(post['id'])}"
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
        vibelyComments = vibely.get(f"authors/{author_pk}/posts/{post_pk}/comments")
        if vibelyComments.status_code == 200:
            for comment in vibelyComments.json()["comments"]:
                allComments.append({
                    "id": comment["id"],
                    "author": serializeVibelyAuthor(comment["author"]),
                    "comment": comment["comment"],
                    "contentType": comment["contentType"],
                    "published": comment["published"],
                    "type": "NodeComment",
                    "post": post_pk,
                })
        socialSyncComments = socialSync.get(f"authors/{author_pk}/posts/{post_pk}/comments")
        if socialSyncComments.status_code == 200:
            for comment in socialSyncComments.json()["comments"]:
                allComments.append({
                    "id": comment["id"],
                    "author": serializeVibelyAuthor(comment["author"]),
                    "comment": comment["comment"],
                    "contentType": comment["contentType"],
                    "published": comment["published"],
                    "type": "NodeComment",
                    "post": post_pk,
                })
        # socialSync_comments = ctrlAltDelete.get(f"authors/{author_pk}/posts/{post_pk}/comments")
        # if socialSync_comments.status_code == 200:
        #     for comment in socialSync_comments.json()["comments"]:
        #         allComments.append({
        #             "id": comment["id"],
        #             "author": serializeVibelyAuthor(comment["author"]),
        #             "comment": comment["comment"],
        #             "contentType": comment["contentType"],
        #             "published": comment["published"],
        #             # "post": comment["post"],
        #         })
        
