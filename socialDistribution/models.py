from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class Author(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField(max_length=255)
    displayName = models.CharField(max_length=255)
    github = models.TextField()
    image = models.ImageField(
        upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.displayName


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(displayName=instance, user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.User.save()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    origin = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contentType = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    published = models.DateTimeField(default=datetime.now)
    owner = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.TextField(blank=True, null=True)
    count = models.IntegerField(default=0)
    visibility = models.CharField(max_length=255, default="PUBLIC")
    unlisted = models.BooleanField(default=False)
    # Posts can be links to images.
    imageOnlyPost = models.BooleanField(default=False)
    image_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/',
                              blank=True, null=True)  # Posts can be images


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commenter = models.ForeignKey(Author, on_delete=models.CASCADE)
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.CharField(max_length=255)
    published = models.DateTimeField()


@receiver(post_save, sender=Comment)
def updateCommentCount(sender, instance, **kwargs):
    post = instance.parentPost
    post.count = post.count + 1
    post.save()


class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='from_author_follow')
    to_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='to_author_follow')
    status = models.CharField(max_length=255)


class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='from_author')
    to_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='to_author')
    status = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # After saving the friend request, trigger the notification
        process_friend_request_notification(self)

class PostLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    published = models.DateTimeField()


class CommentLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE) # maybe dont need it??
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    published = models.DateTimeField()


class ConnectedNode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    teamName = models.CharField(max_length=255)

class Inbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='inbox_recipient')
    sender = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='inbox_sender')
    content = models.TextField()
    type = models.CharField(max_length=255)  # post, like, comment, friend_request
    timestamp = models.DateTimeField(default=datetime.now)
    friend_request_status = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient}: {self.content}"
    

@receiver(post_save, sender=Inbox)
def process_inbox_item(sender, instance, **kwargs):
    """
    Custom signal to process actions when an item is added to the inbox.
    """
    # Need to add more based on inbox item type
    if instance.type == "friend_request":
        process_friend_request_notification(instance)
    
def process_friend_request_notification(instance):
    # To send friend request
    sender = instance.from_author
    recipient = instance.to_author
    content = f"You have a new friend request from {sender.display_name}."

    #Inbox Entry: 
    inbox_item = Inbox.objects.create(
        recipient=recipient,
        sender=sender,
        content=content,
        type="friend_request",
        timestamp=timezone.now(),
        friend_request_status=instance.status,
    )

@receiver(post_save, sender=FriendRequest)
def process_friend_request(sender, instance, **kwargs):
    if instance.status == "PENDING":
        # For Pending Friend Requests
        send_friend_request_notification(instance)
        update_friend_request_counters(instance.to_author)

def send_friend_request_notification(friend_request):
    #Sending Friend request notifications. Called whe n a friend request is pending. 
    pass

def update_friend_request_counters(author):
    # Update Counters for Pending friend requests.
    pass