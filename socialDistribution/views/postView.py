import requests
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework import generics
from django.conf import settings
from drf_spectacular.utils import extend_schema
from socialDistribution.models import Author, Post
from socialDistribution.pagination import Pagination, JsonObjectPaginator
from socialDistribution.serializers import PostSerializer, FollowSerializer, AuthorSerializer
from socialDistribution.util import sendToFriendsInbox, isFriend
import base64
from io import BytesIO
from PIL import Image
from django.http import HttpResponse
from ..util import isFrontendRequest, team1, team2, serializeTeam1Post, sendToEveryonesInbox
import json
from rest_framework.renderers import JSONRenderer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticated]
    pagination_class = JsonObjectPaginator

    @extend_schema(
        tags=['Posts'],
        description='[local, remote] get the recent posts from author AUTHOR_ID (paginated)\
            returns posts from author, their friends, and public posts'
    )
    def get(self, request, author_pk, format=None):
        author = Author.objects.get(pk=author_pk)

        # get posts from author, their friends, and public posts
        authorPosts = Post.objects.filter(author=author)
        publicPosts = Post.objects.filter(visibility="PUBLIC")
        
        authorFriends = FollowSerializer(author.following.filter(status="Accepted"), many=True).data
        authorFriends = [(Author.objects.get(pk=friend["following"]["id"])) for friend in authorFriends]
        friendsPosts = Post.objects.filter(author__in=authorFriends, visibility="FRIENDS")

        all_posts = json.loads(JSONRenderer().render(PostSerializer(authorPosts, many=True).data + 
        PostSerializer(publicPosts, many=True).data + 
        PostSerializer(friendsPosts, many=True).data).decode('utf-8'))

        # get posts from other servers
        if isFrontendRequest(request):
            team1_posts = team1.get(f"authors/{author_pk}/posts/")
            if team1_posts.status_code == 200:
                for post in team1_posts.json()["items"]:
                    all_posts.append(serializeTeam1Post(post))
            team2_posts = team2.get(f"authors/{author_pk}/posts/")
            if team2_posts.status_code == 200:
                for post in team2_posts.json()["items"]:
                    post["author"]["github"] = ""
                    post["categories"] = ""
                    all_posts.append(serializeTeam1Post(post))

        # add source to posts and return everything
        for post in all_posts:
            post["source"] = f"{settings.BASEHOST}/authors/{post['author']['id']}/posts/{post['id']}"
        page = self.paginate_queryset(all_posts)
        return self.get_paginated_response(page)

    @extend_schema(
        tags=['Posts'],
        description='Create a new post but generate a new id'
    )
    def post(self, request, author_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        serializer = PostSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(author=author, origin=f"{settings.BASEHOST}/authors/{author.id}/posts/")
            tempPost = Post.objects.get(pk=serializer.data["id"])
            if tempPost.imageOnlyPost:
                tempPost.unlisted = True
            tempPost.origin = f"{settings.BASEHOST}/authors/{author.id}/posts/{tempPost.id}"
            tempPost.save()

            # TODO: check Inbox for stuff from nodes
            if tempPost.visibility == "FRIENDS":
                sendToFriendsInbox(author, PostSerializer(tempPost).data)
            elif tempPost.visibility == "PUBLIC":
                sendToEveryonesInbox(PostSerializer(tempPost).data)
            
            return Response(PostSerializer(tempPost).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    @extend_schema(
        tags=['Posts'],
        description='Update the post whose id is POST_ID (must be authenticated)'
    )
    def post(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk, author=author)
        if post:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save(author=author, id=post_pk)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Posts'],
        description='create a post where its id is POST_ID'
    )
    def put(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author, id=post_pk)
            sendToFriendsInbox(author, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Posts'],
        description='GET [local, remote] get the public post whose id is POST_ID'
    )
    def get(self, request, author_pk, post_pk, format=None):
        try:
            author = Author.objects.get(pk=author_pk)
        except Author.DoesNotExist:
            if isFrontendRequest(request):
                team1_post = team1.get(f"authors/{author_pk}/posts/{post_pk}/")
                if team1_post.status_code == 200:
                    return Response(serializeTeam1Post(team1_post.json()))
                # team2_post = team2.get("author/posts/" + post_pk)
                team2_post = team2.get(f"authors/{author_pk}/posts/{post_pk}")
                if team2_post.status_code == 200:
                    post = team2_post.json()
                    post["author"]["github"] = ""
                    post["categories"] = ""
                    return Response(serializeTeam1Post(post))
            return Response({"message": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
        
        post = self.get_object(post_pk)

        serializer = PostSerializer(post)
        if post.visibility == 'PUBLIC':
            return Response(serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=['Posts'],
        description='Delete a post'
    )
    def delete(self, request, author_pk, post_pk, format=None):
        post = self.get_object(post_pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageViewSet(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @extend_schema(
        tags=['Posts'],
        description='As an author, I want to be able to make posts that are unlisted, that are publicly shareable by URI alone (or for embedding images)\
            if the post is an image post will return base64 encoded image else return post if it is public or unlisted\
                (unlisted implies pubic post)'
    )
    def get(self, request, post_pk, format=None):
        # TODO: check other groups image only posts
        # if isFrontendRequest(request):
        #     team1_post = team1.get("authors/" + author_pk + "/posts/" + post_pk + "/")
        #     if team1_post.status_code == 200:
        #         return Response(serializeTeam1Post(team1_post.json()))
        #     # team2_post = team2.get("author/posts/" + post_pk)

        post = Post.objects.get(pk=post_pk)
        if post.imageOnlyPost:
            # https://stackoverflow.com/questions/31826335/how-to-convert-pil-image-image-object-to-base64-string
            if post.image_link:
                im = Image.open(requests.get(post.image_link, stream=True).raw)
                buffered = BytesIO()
                im.save(buffered, format="JPEG")
                base64_data = base64.b64encode(buffered.getvalue())
            elif post.image:
                with open(post.image.path, "rb") as img_file:
                    base64_data = base64.b64encode(img_file.read())
            return HttpResponse(base64_data)
        elif post.visibility == 'PUBLIC' or post.unlisted == True:
            serializer = PostSerializer(post)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class PublicPostList(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [
#         permissions.IsAuthenticated]
#     pagination_class = JsonObjectPaginator

#     # @extend_schema(
#     #     tags=['Posts'],
#     #     # TODO: check if 'everyone' implies posts fromo other servers
#     #     description='As an author I should be able to browse the public posts of everyone'
#     # )
#     # def get(self, request, format=None):
#     #     posts = Post.objects.filter(visibility="PUBLIC")
#     #     all_posts = json.loads(JSONRenderer().render(PostSerializer(posts, many=True).data).decode('utf-8'))
#     #     if isFrontendRequest(request):
#     #         team1_posts = team1.get(f"posts/")
#     #         if team1_posts.status_code == 200:
#     #             for post in team1_posts.json()["items"]:
#     #                 all_posts.append(serializeTeam1Post(post))
#     #         # team2_posts = team2.get("author/posts/" + author_pk)

#     #     for post in all_posts:
#     #         post["source"] = request.headers['Host'] + '/authors/' + post["author"]["id"] + '/posts/' + post["id"]
#     #     page = self.paginate_queryset(all_posts)
#     #     return self.get_paginated_response(page)

