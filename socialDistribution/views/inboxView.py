from socialDistribution.models import Inbox, Author, Post, Comment
from socialDistribution.serializers import InboxSerializer, PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
import json
from ..util import isFrontendRequest, serializeTeam1Post, serializeTeam1Author


def handlePostItem(newItem):
    post = serializeTeam1Post(newItem)
    # create the post object
    newPost = Post.objects.create(
        id=post["id"],
        title=post["title"],
        source=post["source"],
        origin=post["origin"],
        description=post["description"],
        contentType=post["contentType"],
        content=post["content"],
        author=post["author"],
        categories=post["categories"],
        count=post["count"],
        size=post["size"],
        visibility=post["visibility"],
        unlisted=post["unlisted"],
        published=post["published"],
    )
    return PostSerializer(newPost).data


def handleCommentItem(newItem):
    comment = {
        "id": newItem["id"],
        "author": serializeTeam1Author(newItem["author"]),
        "comment": newItem["comment"],
        "contentType": newItem["contentType"],
        "published": newItem["published"],
        # "post": comment["post"],
    }
    newComment = Comment.objects.create(
        id=comment["id"],
        author=comment["author"],
        comment=comment["comment"],
        contentType=comment["contentType"],
        published=comment["published"],
    )
    return CommentSerializer(newComment).data


def handleFollowItem(newItem):
    follow = {
        "id": newItem["id"],
        "actor": serializeTeam1Author(newItem["actor"]),
        "object": serializeTeam1Author(newItem["object"]),
        "published": newItem["published"],
    }
    newFollow = Follow.objects.create(
        id=follow["id"],
        actor=follow["actor"],
        object=follow["object"],
        published=follow["published"],
    )
    return FollowSerializer(newFollow).data


def handleLikeItem(newItem):
    like = {
        "id": newItem["id"],
        "author": serializeTeam1Author(newItem["author"]),
        "object": serializeTeam1Post(newItem["object"]),
        "published": newItem["published"],
    }
    newLike = PostLike.objects.create(
        id=like["id"],
        author=like["author"],
        object=like["object"],
        published=like["published"],
    )
    return PostLikeSerializer(newLike).data


class InboxItemView(generics.GenericAPIView):
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        tags=["Inbox"],
        description="Get all inbox items for the current user.",
    )
    def get(self, request, author_pk, *args, **kwargs):
        author = Author.objects.get(pk=author_pk)
        inbox = Inbox.objects.get(author=author)
        serializer = InboxSerializer(inbox)

        allItems = json.loads(inbox.items)
        result = []
        for item in allItems:
            result.append(json.loads(item))

        copy = serializer.data
        copy["items"] = result
        return Response(copy, status=status.HTTP_200_OK)
    
    @extend_schema(
        tags=["Inbox"],
        description="Create a new inbox item for the current user.(author_id is the recipient). \
            You must send a json.dumps(object) string in the `items` field. Just the object not a list or anything",
    )
    def post(self, request, author_pk, *args, **kwargs):
        """
        json_string = json.dumps(data)
        escaped_json_string = json_string.replace('"', '\\"')
        final_format_string = f'"{escaped_json_string}"'
        """
        # TODO: TEST IF IT WORKS

        try:
            author = Author.objects.get(pk=author_pk)
        except:
            return Response({"message": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

        inbox = Inbox.objects.get(author=author)
        items = json.loads(inbox.items)
        newItem = request.data['item']

        if not isFrontendRequest(request):
            if newItem["type"].lower() == "follow":
                items.append(handleFollowItem(newItem))
            elif newItem["type"].lower() == "like":
                items.append(handleLikeItem(newItem))
            elif newItem["type"].lower() == "comment":
                items.append(handleCommentItem(newItem))
            elif newItem["type"].lower() == "post":
                items.append(handlePostItem(newItem))

        inbox.items = json.dumps(items, default=str)
        inbox.save()
        return Response({"message": "Item Added to inbox!"}, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        tags=["Inbox"],
        description="Delete all inbox items for the current user.(author_id is the recipient)",
    )
    def delete(self, request, author_id, *args, **kwargs):
        # TODO: TEST IF IT WORKSS
        author = Author.objects.get(pk=author_id)
        inbox = Inbox.objects.filter(author=author)
        inbox.items = json.dumps([])
        return Response({'message': "Inbox Cleared!"}, status=status.HTTP_204_NO_CONTENT)
