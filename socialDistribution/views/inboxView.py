from socialDistribution.models import Inbox, Author
from socialDistribution.serializers import InboxSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from drf_spectacular.utils import extend_schema
import json


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
        # TODO: TEST IF IT WORKSS
        author = Author.objects.get(pk=author_pk)
        inbox = Inbox.objects.get(author=author)
        items = json.loads(inbox.items)
        newItems = json.loads(request.data['items'])
        items.append(json.dumps(newItems, default=str))
        inbox.items = json.dumps(items)
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
