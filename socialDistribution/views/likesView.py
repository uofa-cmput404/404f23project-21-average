from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from socialDistribution.models import Author, Comment, CommentLike, Post, PostLike
from ..util import vibely, serializeVibelyPost, serializeVibelyAuthor, socialSync, ctrlAltDelete, isFrontendRequest
from socialDistribution.serializers import CommentLikeSerializer, PostLikeSerializer
from socialDistribution.util import addToInbox
from ..pagination import JsonObjectPaginator
import json
from rest_framework.renderers import JSONRenderer


class AddLikeToPostView(generics.ListCreateAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = JsonObjectPaginator

    @extend_schema(
        tags=['Likes'],
        description='GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID'
    )
    def get(self, request, author_pk, post_pk, format=None):
        allLikes = []
        try:
            post = Post.objects.get(pk=post_pk)
            likes = PostLike.objects.filter(post=post)
            allLikes = json.loads(JSONRenderer().render(PostLikeSerializer(likes, many=True).data).decode('utf-8'))
        except:
            if isFrontendRequest(request):
                # TODO: check that this works
                vibelyLikes = vibely.get(f"authors/{author_pk}/posts/{post_pk}/likes/")
                # print(vibelyLikes.text)
                if vibelyLikes.status_code == 200:
                    for like in vibelyLikes.json()["items"]:
                        allLikes.append({
                            "object": like["object"],
                            "author": serializeVibelyAuthor(like["author"]),
                            "post": post_pk,
                            # "published": like["published"],
                            "type": like["type"],
                            # "context": like["@context"],
                            "summary": like["summary"],
                            
                        })
                
                socialSyncLikes = socialSync.get(f"authors/{author_pk}/posts/{post_pk}/likes")
                print(socialSyncLikes.text)
                if socialSyncLikes.status_code == 200 and socialSyncLikes.text != "[]":
                    for like in socialSyncLikes.json():
                        allLikes.append({
                            "author": serializeVibelyAuthor(like["author"]),
                            "post": post_pk,
                            "type": like["type"],
                            "context": like["@context"],
                            "object": like["object"],
                            "summary": like["summary"],
                        })

                ctrlAltDeleteLikes = ctrlAltDelete.get(f"authors/{author_pk}/posts/{post_pk}/likes/")
                if ctrlAltDeleteLikes.status_code == 200:
                    for like in ctrlAltDeleteLikes.json()["items"]:
                        allLikes.append({
                            "object": like["object"],
                            "author": serializeVibelyAuthor(like["author"]),
                            "post": post_pk,
                            # "published": like["published"],
                            "type": like["type"],
                            "context": like["context"],
                            "summary": like["summary"],
                        })
            else:
                return Response({"message": "no likes found"}, status=status.HTTP_404_NOT_FOUND)

        print(allLikes)
        page = self.paginate_queryset(allLikes)
        return self.get_paginated_response(page)

    @extend_schema(
        tags=['Likes'],
        description='add a like to post from AUTHOR_ID on POST_ID'
    )
    def post(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk)
        if not post:
            return Response({"message": "post not found"}, status=status.HTTP_404_NOT_FOUND)

        # check if author already liked the post
        if PostLike.objects.filter(author=author, post=post).exists():
            return Response({"message": "cannot like post again"}, status=status.HTTP_400_BAD_REQUEST)

        # can only like a friends only post or public post
        # if (post.visibility == "FRIENDS" and isFriend(author, post.author)) or post.visibility == "PUBLIC":
        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author, post=post)

            # send like to post owners inbox
            addToInbox(post.author, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"message": "insufficient permissions to like psot"}, status=status.HTTP_403_FORBIDDEN)


class AddLikeToCommentView(generics.ListCreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = JsonObjectPaginator

    @extend_schema(
        tags=['Likes'],
        description='add a like to comment from AUTHOR_ID on COMMENT_ID'
    )
    def post(self, request, author_pk, post_pk, comment_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk)
        comment = Comment.objects.get(pk=comment_pk, post=post)

        # check if author already liked the post
        if CommentLike.objects.filter(author=author, comment=comment).exists():
            return Response({"message": "cannot like comment again"}, status=status.HTTP_400_BAD_REQUEST)

        # can only like public comments
        if post.visibility == "PUBLIC":
            serializer = CommentLikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=author, comment=comment)
                
                # send like to comment owners inbox
                addToInbox(comment.author, serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"message": "cannot like comment"}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=['Likes'],
        description='GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID comment COMMENT_ID'
    )
    def get(self, request, author_pk, post_pk, comment_pk, format=None):
        # TODO: check how it exactly works with remote authors
        allLikes = []
        try:
            comment = Comment.objects.get(pk=comment_pk)
            likes = CommentLike.objects.filter(comment=comment)
            allLikes = json.loads(JSONRenderer().render(CommentLikeSerializer(likes, many=True).data).decode('utf-8'))
        except:
            if isFrontendRequest(request):
                vibelyLikes = vibely.get(f"authors/{author_pk}/posts/{post_pk}/comments/{comment_pk}/likes")
                if vibelyLikes.status_code == 200:
                    for like in vibelyLikes.json()["items"]:
                        allLikes.append({
                            "id": like["id"],
                            "author": serializeVibelyAuthor(like["author"]),
                            "comment": serializeVibelyPost(like["comment"]),
                            "published": like["published"],
                            "type": like["type"],
                        })

                socialSyncLikes = socialSync.get(f"authors/{author_pk}/posts/{post_pk}/comments/{comment_pk}/likes")
                if socialSyncLikes.status_code == 200 and socialSyncLikes.text != "[]":
                    for like in socialSyncLikes.json()["items"]:
                        allLikes.append({
                            "id": like["id"],
                            "author": serializeVibelyAuthor(like["author"]),
                            "comment": serializeVibelyPost(like["comment"]),
                            "published": like["published"],
                            "type": like["type"],
                        })
                
                # ctrlAltDeleteLikes = ctrlAltDelete.get(f"authors/{author_pk}/posts/{post_pk}/comments/{comment_pk}/likes")
                # if ctrlAltDeleteLikes.status_code == 200:
                #     likes = ctrlAltDeleteLikes.json()["likes"]

        page = self.paginate_queryset(allLikes)
        return self.get_paginated_response(page)


class GetAllAuthorLikes(generics.ListAPIView):
    queryset1 = PostLike.objects.all()
    queryset2 = CommentLike.objects.all()
    serializer_class1 = PostLikeSerializer
    serializer_class2 = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = JsonObjectPaginator

    @extend_schema(
        tags=['Likes'],
        description='GET [local, remote] list what public things AUTHOR_ID liked.'
    )
    def get(self, request, author_pk, format=None):
        # if i call that endpoint to ur server i should also check to see if theres any public likes from that author on my server
        try:
            author = Author.objects.get(pk=author_pk)
        except:
            # try to find the author on vibely
            vibelyRemoteAuthor = vibely.get(f"authors/{author_pk}")
            if vibelyRemoteAuthor.status_code == 200:
                likes = vibely.get(f"authors/{author_pk}/liked/")
                if likes.status_code == 200:
                    return Response(likes.json())
            ctrlAltDeleteRemoteAuthor = ctrlAltDelete.get(f"authors/{author_pk}")
            if ctrlAltDeleteRemoteAuthor.status_code == 200:
                likes = ctrlAltDelete.get(f"authors/{author_pk}/liked/")
                if likes.status_code == 200:
                    return Response(likes.json())
            # try to find the author on socialSync
            socialSyncRemoteAuthor = socialSync.get(f"authors/{author_pk}")
            if socialSyncRemoteAuthor.status_code == 200:
                likes = socialSync.get(f"authors/{author_pk}/liked/")
                if likes.status_code == 200:
                    return Response(likes.json())
            return Response({"message": "author not found"}, status=status.HTTP_404_NOT_FOUND)

        postLikes = PostLike.objects.filter(author_id=author_pk, post__visibility='PUBLIC')
        commentLikes = CommentLike.objects.filter(author=author, comment__post__visibility='PUBLIC')
        if postLikes or commentLikes:
            return Response({"type":"liked",
            "items": PostLikeSerializer(postLikes, many=True).data + CommentLikeSerializer(commentLikes, many=True).data})

        return Response({"message": "no likes found"}, status=status.HTTP_200_OK)
