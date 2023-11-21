from socialDistribution.models import Inbox
from socialDistribution.serializers import InboxSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema


class InboxItemView(APIView):
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        tags=["Inbox"],
        description="Get all inbox items for the current user.",
    )
    def get(self, request, author_id, *args, **kwargs):
        inbox = Inbox.objects.filter(recipient=request.user.author)
        serializer = InboxSerializer(inbox, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        tags=["Inbox"],
        description="Create a new inbox item for the current user.(author_id is the recipient)",
    )
    def post(self, request, author_id, *args, **kwargs):
        inbox = Inbox.objects.filter(recipient=author_id)
        serializer = InboxSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        tags=["Inbox"],
        description="Delete all inbox items for the current user.(author_id is the recipient)",
    )
    def delete(self, request, author_id, *args, **kwargs):
        inbox = Inbox.objects.filter(recipient=request.user.author)
        inbox.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @receiver(post_save, sender=Inbox)
    # def process_inbox_item(sender, instance, **kwargs):
    #     """
    #     Custom signal to process actions when an item is added to the inbox.
    #     For example, send notifications, update counters, etc.
    #     """
    #     # Need to add more based on inbox item type
    #     if instance.type == "friend_request":
    #         process_friend_request_notification(instance)

    # def process_friend_request_notification(instance):
    #     # To send friend request
    #     sender = instance.from_author
    #     recipient = instance.to_author
    #     content = f"You have a new friend request from {sender.display_name}."

    #     # Send the Friend Request
    #     friend_request = FriendRequest.objects.create(
    #         from_author=sender,
    #         to_author=recipient,
    #         status=instance.status,
    #     )

    #     # Inbox Entry:
    #     inbox_item = Inbox.objects.create(
    #         recipient=recipient,
    #         sender=sender,
    #         content=content,
    #         type="friend_request",
    #         timestamp=timezone.now(),
    #         friend_request_status=instance.status,
    #     )

    #     print(f"Notification: {sender.display_name} sent a friend request to {recipient.display_name}")
    
