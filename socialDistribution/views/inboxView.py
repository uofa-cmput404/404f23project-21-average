from socialDistribution.models import Inbox, Author, Post, Comment, Follow, PostLike
from socialDistribution.serializers import *
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
import json
import uuid
from ..util import isFrontendRequest, serializeTeam1Post, serializeTeam1Author, getUUID


def handlePostItem(newItem):
    # TODO: maybe dont need to save post on db???
    return {
        "id": newItem["id"],
        "title": newItem["title"],
        "type": "newItem",
        "source": newItem["source"],
        "origin": newItem["origin"],
        "description": newItem["description"],
        "contentType": newItem["contentType"],
        "visibility": newItem["visibility"],
        "unlisted": newItem["unlisted"],
        "content": newItem["content"],
        "published": newItem["published"],
        "author": serializeTeam1Author(newItem["author"]),
        "categories": newItem["categories"],
        "image_link": None,
        "image": None,
        "imageOnlyPost": None,
        # "count": post["count"],
        "comments": newItem["comments"]
    }
    # post = serializeTeam1Post(newItem)
    # return post


def handleCommentItem(newItem):
    authorJson = serializeTeam1Author(newItem["author"])
    comment = {
        "id": newItem["id"].split("/")[-1],
        "author": authorJson,
        "comment": newItem["comment"],
        "contentType": newItem["contentType"],
        "published": newItem["published"],
        "type": "NodeComment",
        # "post": comment["post"],
    }
    return comment


def handleFollowItem(newItem):
    # object key must be an author on my server
    # actor key is the foreign_author following my object
    # actor is requesting to follow object
    actorJson = serializeTeam1Author(newItem["actor"])
    actorJson["type"] = "NodeAuthor"
    actorJson["id"] = getUUID(newItem["actor"]["id"])
    try:
        actingAuthor = Author.objects.get(pk=actorJson["id"])
    except:
        actingAuthor = Author.objects.create(**actorJson)
    
    try:
        foreign_author = Author.objects.get(pk=getUUID(newItem["object"]["id"]))
    except:
        raise Exception("Object Author not found")

    # author is requesting to follow foreign_author
    follow = {
        "type": "follow",
        "summary": f"{actingAuthor.username} wants to follow {foreign_author.username}",
        "actor": AuthorSerializer(foreign_author).data,
        "object": AuthorSerializer(actingAuthor).data,
    }
    return follow


def handleLikeItem(newItem):
    authorJson = serializeTeam1Author(newItem["author"])
    likeJson = {
        # "id": newItem["id"].split("/")[-1],
        "author": authorJson,
        "summary": newItem["summary"],
        "context": newItem["context"],
        "object": newItem["object"],
        "type": "Like",
    }

    # return PostLikeSerializer(newLike[0]).data
    return likeJson


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
        newItem = request.data['items']

        if not isFrontendRequest(request):
            if newItem["type"].lower() == "follow":
                try:
                    items.append(json.dumps(handleFollowItem(newItem), default=str))
                except Exception as e:
                    print(e)
                    return Response({"message": "Object Author not found"}, status=status.HTTP_404_NOT_FOUND)
            elif newItem["type"].lower() == "like":
                items.append(json.dumps(handleLikeItem(newItem), default=str))
            elif newItem["type"].lower() == "comment":
                items.append(json.dumps(handleCommentItem(newItem), default=str))
            elif newItem["type"].lower() == "post":
                items.append(json.dumps(handlePostItem(newItem), default=str))
        else:
            return Response({"message": "Only Nodes can request to inbox"}, status=status.HTTP_400_BAD_REQUEST)

        inbox.items = json.dumps(items, default=str)
        inbox.save()
        return Response({"message": "Item Added to inbox!"}, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        tags=["Inbox"],
        description="Delete all inbox items for the current user.(author_id is the recipient)",
    )
    def delete(self, request, author_pk, *args, **kwargs):
        # TODO: TEST IF IT WORKSS
        author = Author.objects.get(pk=author_pk)
        inbox = Inbox.objects.get(author=author)
        inbox.items = json.dumps([])
        inbox.save()
        return Response({'message': "Inbox Cleared!"}, status=status.HTTP_204_NO_CONTENT)
