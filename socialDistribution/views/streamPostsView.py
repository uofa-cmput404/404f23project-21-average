from rest_framework import permissions
from rest_framework import generics
from django.conf import settings
from drf_spectacular.utils import extend_schema
from socialDistribution.models import Author, Post
from socialDistribution.pagination import  JsonObjectPaginator
from socialDistribution.serializers import PostSerializer, FollowSerializer
from socialDistribution.util import  serializeVibelyAuthor
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
            if vibelyPosts.status_code == 200:
                for post in vibelyPosts.json()["items"]:
                    res.append(serializeVibelyPost(post))

    socialSyncAuthors = socialSync.get("authors/")
    if socialSyncAuthors.status_code == 200:
        for author in socialSyncAuthors.json()["items"]:
            author2 = serializeVibelyAuthor(author)
            socialSyncPosts = socialSync.get(f"authors/{getUUID(author2['id'])}/posts")
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
