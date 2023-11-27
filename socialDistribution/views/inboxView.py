from socialDistribution.models import Inbox, Author, Post, Comment, Follow, PostLike
from socialDistribution.serializers import *
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
import json
from ..util import isFrontendRequest, serializeTeam1Post, serializeTeam1Author


def handlePostItem(newItem):
    post = serializeTeam1Post(newItem)
    authorJson = serializeTeam1Author(newItem["author"])
    authorJson["type"] = "NodeAuthor"
    author = Author.objects.get_or_create(**authorJson)
    # print(author[0])
    # print(AuthorSerializer(author[0]).data)
    # create the post object
    newPost = Post.objects.get_or_create(
        id=post["id"],
        title=post["title"],
        source=post["source"],
        type="NodePost",
        origin=post["origin"],
        description=post["description"],
        contentType=post["contentType"],
        content=post["content"],
        author=author[0],
        categories=','.join(post["categories"]),
        count=post["count"],
        visibility=post["visibility"],
        unlisted=post["unlisted"],
        published=post["published"],
    )
    return PostSerializer(newPost[0]).data


def handleCommentItem(newItem):
    authorJson = serializeTeam1Author(newItem["author"])
    authorJson["type"] = "NodeAuthor"
    author = Author.objects.get_or_create(**authorJson)
    comment = {
        "id": newItem["id"].split("/")[-1],
        "author": author[0],
        "comment": newItem["comment"],
        "contentType": newItem["contentType"],
        "published": newItem["published"],
        "type": "NodeComment",
        # "post": comment["post"],
    }
    newComment = Comment.objects.get_or_create(**comment)
    return CommentSerializer(newComment[0]).data


def handleFollowItem(newItem):
    # object key must be an author on my server
    # actor key is the foreign_author following my object
    # actor is requesting to follow object
    actorJson = serializeTeam1Author(newItem["actor"])
    actorJson["type"] = "NodeAuthor"
    author = Author.objects.get_or_create(**actorJson)

    objectJson = serializeTeam1Author(newItem["object"])
    # print(f"{objectJson['id']}")
    foreign_author = Author.objects.get(pk=objectJson["id"])

    # author is requesting to follow foreign_author
    follow = {
        "follower": author[0],
        "following": foreign_author,
        "status": "Pending",
        "summary": newItem["summary"],
    }
    newFollow = Follow.objects.get_or_create(**follow)
    return FollowSerializer(newFollow[0]).data


def handleLikeItem(newItem):
    authorJson = serializeTeam1Author(newItem["author"])
    authorJson["type"] = "NodeAuthor"
    author = Author.objects.get_or_create(**authorJson)
    
    if newItem["summary"].split()[-1] == "post":
        like = {
        "context": newItem["context"],
        "author": author[0],
        "object": newItem["object"],
        "type": "NodePostLike",
        "summary": newItem["summary"],
        }
        newLike = PostLike.objects.get_or_create(**like)
    elif newItem["summary"].split()[-1] == 'comment':
        like = {
        "context": newItem["context"],
        "author": author[0],
        "object": newItem["object"],
        "type": "NodeCommentLike",
        "summary": newItem["summary"],
        }
        newLike = CommentLike.objects.get_or_create(**like)

    return PostLikeSerializer(newLike[0]).data


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
                items.append(json.dumps(handleFollowItem(newItem), default=str))
            elif newItem["type"].lower() == "like":
                items.append(json.dumps(handleLikeItem(newItem), default=str))
            elif newItem["type"].lower() == "comment":
                items.append(json.dumps(handleCommentItem(newItem), default=str))
            elif newItem["type"].lower() == "post":
                items.append(json.dumps(handlePostItem(newItem), default=str))
        else:
            return Response({"message": "Only Nodes can request to inbox"}, status=status.HTTP_400_BAD_REQUEST)

        inbox.items = json.dumps(items, default=str)
        print(inbox.items)
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
        print(inbox.items)
        inbox.items = json.dumps([])
        inbox.save()
        return Response({'message': "Inbox Cleared!"}, status=status.HTTP_204_NO_CONTENT)
