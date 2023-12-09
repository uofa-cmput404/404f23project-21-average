from rest_framework.response import Response
from socialDistribution.models import Author, Inbox, Follow
from socialDistribution.serializers import AuthorSerializer, InboxSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
import json
from ..util import isFrontendRequest, serializeVibelyAuthor, getUUID
from django.http import JsonResponse


def handlePostItem(newItem):
    return {
        "id": newItem["id"],
        "title": newItem["title"],
        "type": "post",
        "source": newItem["source"],
        "origin": newItem["origin"],
        "description": newItem["description"],
        "contentType": newItem["contentType"],
        "visibility": newItem["visibility"],
        "unlisted": newItem["unlisted"],
        "content": newItem["content"],
        "published": newItem["published"],
        "author": serializeVibelyAuthor(newItem["author"]),
        "categories": newItem["categories"],
        "image_link": None,
        "image": None,
        "imageOnlyPost": None,
        # "count": post["count"],
        "comments": newItem["comments"]
    }


def handleCommentItem(newItem):
    authorJson = serializeVibelyAuthor(newItem["author"])
    comment = {
        "id": newItem["id"].split("/")[-1],
        "author": authorJson,
        "comment": newItem["comment"],
        "contentType": newItem["contentType"],
        "published": newItem["published"],
        "type": "Comment",
    }
    return comment


def handleFollowItem(newItem):
    # object key must be an author on my server
    # actor key is the foreign_author following my object
    # actor is requesting to follow object
    actorJson = serializeVibelyAuthor(newItem["actor"])
    actorJson["type"] = "NodeAuthor"
    actorJson["id"] = getUUID(newItem["actor"]["id"])
    try:
        actingAuthor = Author.objects.get(pk=actorJson["id"])
    except:
        actingAuthor = Author.objects.create(**actorJson)
    
    try:
        foreignAthorID = getUUID(newItem["object"]["id"])
        foreign_author = Author.objects.filter(pk=foreignAthorID)[0]
    except:
        raise Exception("Object Author not found")

    # author is requesting to follow foreign_author
    follow = {
        "type": "follow",
        "summary": f"{actingAuthor.username} wants to follow {foreign_author.username}",
        "actor": AuthorSerializer(foreign_author).data,
        "object": AuthorSerializer(actingAuthor).data,
    }
    x = Follow.objects.create(following=foreign_author, follower=actingAuthor, summary=follow["summary"])
    x.save()
    return follow


def handleLikeItem(newItem):
    authorJson = serializeVibelyAuthor(newItem["author"])
    likeJson = {
        "author": authorJson,
        "summary": newItem["summary"],
        "context": newItem["context"],
        "object": newItem["object"],
        "type": "Like",
    }
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
                    return JsonResponse({
                        "message": "Object Author not found",
                        'exception': str(e),
                        'req': request,
                        'author': author_pk
                        },
                         status=status.HTTP_404_NOT_FOUND)
            elif newItem["type"].lower() == "like":
                items.append(json.dumps(handleLikeItem(newItem), default=str))
            elif newItem["type"].lower() == "comment":
                items.append(json.dumps(handleCommentItem(newItem), default=str))
            elif newItem["type"].lower() == "post":
                items.append(json.dumps(handlePostItem(newItem), default=str))
        else:
            # Only implement inbox for nodes b/c this will be done manually for local authors
            return Response({"message": "Only Nodes can request to inbox"}, status=status.HTTP_400_BAD_REQUEST)

        inbox.items = json.dumps(items, default=str)
        inbox.save()
        return Response({"message": "Item Added to inbox!"}, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        tags=["Inbox"],
        description="Delete all inbox items for the current user.(author_id is the recipient)",
    )
    def delete(self, request, author_pk, *args, **kwargs):
        author = Author.objects.get(pk=author_pk)
        inbox = Inbox.objects.get(author=author)
        inbox.items = json.dumps([])
        inbox.save()
        return Response({'message': "Inbox Cleared!"}, status=status.HTTP_204_NO_CONTENT)
