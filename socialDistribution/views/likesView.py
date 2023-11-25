from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from socialDistribution.models import Author, Comment, CommentLike, Post, PostLike
from socialDistribution.pagination import Pagination
from ..util import isFrontendRequest, team1, team2, serializeTeam1Post
from socialDistribution.serializers import CommentLikeSerializer, PostLikeSerializer
from socialDistribution.util import addToInbox


class AddLikeToPostView(generics.ListCreateAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @extend_schema(
        tags=['Likes'],
        description='GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID'
    )
    def get(self, request, author_pk, post_pk, format=None):
        post = Post.objects.get(pk=post_pk)
        likes = PostLike.objects.filter(post=post)
        if isFrontendRequest(request):
            if not likes:
                team1_likes = team1.get(f"authors/{author_pk}/posts/{post_pk}/likes/")
                if team1_likes.status_code == 200:
                    for like in team1_likes.json()["likes"]:
                        likes.append({
                            "id": like["id"],
                            "author": serializeTeam1Author(like["author"]),
                            "post": serializeTeam1Post(like["post"]),
                            "published": like["published"],
                            "type": like["type"],
                        })
                team2_likes = team2.get(f"authors/{author_pk}/posts/{post_pk}/likes")
                if team2_likes.status_code == 200:
                    for like in team2_likes.json()["likes"]:
                        likes.append({
                            "id": like["id"],
                            "author": serializeTeam1Author(like["author"]),
                            "post": serializeTeam1Post(like["post"]),
                            "published": like["published"],
                            "type": like["type"],
                        })
        page = self.paginate_queryset(likes)
        serializer = PostLikeSerializer(likes, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(
        tags=['Likes'],
        description='add a like to comment from AUTHOR_ID on POST_ID'
    )
    def post(self, request, author_pk, post_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        post = Post.objects.get(pk=post_pk)

        # check if author already liked the post
        if PostLike.objects.filter(author=author, post=post).exists():
            return Response({"message": "cannot like post again"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author, post=post)

            # send like to post owners inbox
            addToInbox(post.author, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddLikeToCommentView(generics.ListCreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

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

        serializer = CommentLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=author, comment=comment)
            
            # send like to comment owners inbox
            addToInbox(comment.author, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=['Likes'],
        description='GET [local, remote] a list of likes from other authors on AUTHOR_ID’s post POST_ID comment COMMENT_ID'
    )
    def get(self, request, author_pk, post_pk, comment_pk, format=None):
        # TODO: check how it exactly works with remote authors
        comment = Comment.objects.get(pk=comment_pk)
        likes = CommentLike.objects.filter(comment=comment)

        page = self.paginate_queryset(likes)
        serializer = CommentLikeSerializer(likes, many=True)
        return self.get_paginated_response(serializer.data)


class GetAllAuthorLikes(generics.ListAPIView):
    queryset1 = PostLike.objects.all()
    queryset2 = CommentLike.objects.all()
    serializer_class1 = PostLikeSerializer
    serializer_class2 = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @extend_schema(
        tags=['Likes'],
        description='GET [local, remote] list what public things AUTHOR_ID liked.'
    )
    def get(self, request, author_pk, format=None):
        # TODO: check if authourID can be a remote author
        # if i call that endpoint to ur server i should also check to see if theres any public likes from that author on my server
        try:
            author = Author.objects.get(pk=author_pk)
        except:
            return Response({"message": "author not found"}, status=status.HTTP_404_NOT_FOUND)
        
        posts = Post.objects.filter(visibility="PUBLIC")

        postLikes = PostLike.objects.filter(author_id=author_pk, post__visibility='PUBLIC')
        commentLikes = CommentLike.objects.filter(author=author, comment__post__visibility='PUBLIC')
        if postLikes or commentLikes:
            return Response(PostLikeSerializer(postLikes, many=True).data + CommentLikeSerializer(commentLikes, many=True).data)

        return Response({"message": "no likes found"}, status=status.HTTP_200_OK)
