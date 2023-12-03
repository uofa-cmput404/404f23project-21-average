from rest_framework import permissions
from rest_framework.response import Response
from socialDistribution.models import Author, Comment, Post
from socialDistribution.pagination import JsonObjectPaginator
from socialDistribution.serializers import CommentSerializer
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from socialDistribution.util import addToInbox, vibely, serializeVibelyAuthor, isFriend, socialSync, ctrlAltDelete, serializeCtrlAltDeleteAuthor


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
        # As an author, comments on friend posts are private only to me the original author.
        author = Author.objects.get(pk=author_pk)
        allComments = []
        try:
            post = Post.objects.get(pk=post_pk)

            comments = []
            if post.visibility == "PUBLIC":
                comments = Comment.objects.filter(post=post_pk)
            elif post.visibility == "FRIENDS" and isFriend(author, post.author):
                comments = Comment.objects.filter(post=post_pk)
            elif request.user.id == post.author.id and author.id == post.author.id and post.visibility == "PRIVATE":
                comments = Comment.objects.filter(post=post_pk)

            allComments = CommentSerializer(comments, many=True).data
        except:
            vibelyComments = vibely.get(f"authors/{author_pk}/posts/{post_pk}/comments")
            if vibelyComments.status_code == 200:
                allComments = []
                for comment in vibelyComments.json()["comments"]:
                    allComments.append({
                        "id": comment["id"],
                        "author": serializeVibelyAuthor(comment["author"]),
                        "comment": comment["comment"],
                        "contentType": comment["contentType"],
                        "published": comment["published"],
                        "type": "comment",
                        "post": post_pk,
                    })
            socialSyncComments = socialSync.get(f"authors/{author_pk}/posts/{post_pk}/comments")
            print(socialSyncComments.text)
            if socialSyncComments.status_code == 200 and socialSyncComments.json():
                for comment in socialSyncComments.json()["items"]:
                    allComments.append({
                        "id": comment["id"],
                        "author": serializeVibelyAuthor(comment["author"]),
                        "comment": comment["comment"],
                        "contentType": comment["contentType"],
                        "published": comment["published"],
                        "type": "NodeComment",
                        "post": post_pk,
                    })
            # TODO: ctrlAltDelete not implemented yet
            # ctrlAltDeleteComments = ctrlAltDelete.get(f"authors/{author_pk}/posts/{post_pk}/comments")
            # if ctrlAltDeleteComments.status_code == 200:
            #     for comment in ctrlAltDeleteComments.json()["comments"]:
            #         allComments.append({
            #             "id": comment["id"],
            #             "author": serializeCtrlAltDeleteAuthor(comment["author"]),
            #             "comment": comment["comment"],
            #             "contentType": comment["contentType"],
            #             "published": comment["published"],
            #             "post": post_pk,
            #         })
        
        if not allComments:
            return Response({'message': 'No Comments found'}, status=status.HTTP_404_NOT_FOUND)
        
        page = self.paginate_queryset(allComments)
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
    
