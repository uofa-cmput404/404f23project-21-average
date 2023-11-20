from django.dispatch import receiver
from socialDistribution.models import Inbox
from socialDistribution.serializers import InboxSerializer
from rest_framework.response import Response
from socialDistribution.models import Author, ConnectedNode, Follow, FriendRequest
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from drf_spectacular.utils import extend_schema


class InboxItemView(APIView):
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer
    
    

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