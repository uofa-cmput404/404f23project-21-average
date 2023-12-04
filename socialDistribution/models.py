from datetime import datetime
import json
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class Author(AbstractUser):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=255)
    # id1 = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, default="author")
    host = models.CharField(max_length=255, blank=True, null=True)
    displayName = models.CharField(max_length=255, blank=True, null=True, default="User")
    github = models.TextField(blank=True, null=True)
    profileImage = models.ImageField(
        upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username


@receiver(post_save, sender=Author)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        Inbox.objects.create(author=instance)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=255, default="post")
    title = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    origin = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contentType = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    published = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    categories = models.TextField(blank=True, null=True, default="web")
    count = models.IntegerField(default=0)
    visibility = models.CharField(max_length=255, default="PUBLIC")
    # unlisted post is a public post
    unlisted = models.BooleanField(default=False)

    # Posts can be links to images.
    imageOnlyPost = models.BooleanField(default=False)
    image_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='post_images/',
                              blank=True, null=True)  # Posts can be images

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=255, default="comment")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    comment = models.TextField()
    contentType = models.CharField(max_length=255)
    published = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.comment, self.author


@receiver(post_save, sender=Comment)
def updateCommentCount(sender, instance, **kwargs):
    post = instance.post
    if post:
        post.count = post.count + 1
        post.save()


class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    summary = models.TextField(blank=True, null=True, default="Follow Request")
    type = models.CharField(max_length=255, default="follow")
    following = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='following')
    published = models.DateTimeField(default=datetime.now)
    # Pending and Accepted
    status = models.CharField(max_length=255, default="Pending")
    

class PostLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=255, default="like")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', null=True)
    summary = models.TextField(blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    object = models.TextField(blank=True, null=True)
    published = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.summary = f"{self.author.username} likes your post"
        super(PostLike, self).save(*args, **kwargs)


class CommentLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=255, default="like")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comment_likes')
    summary = models.TextField(blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    object = models.TextField(blank=True, null=True)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE) # maybe dont need it??
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True)
    published = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.summary = f"{self.author.username} likes your comment"
        super(CommentLike, self).save(*args, **kwargs)


class ConnectedNode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    url = models.CharField(max_length=255)
    teamName = models.CharField(max_length=255)
    api_user = models.ForeignKey(Author, on_delete=models.CASCADE)


class Inbox(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='inbox')
    items = models.TextField(null=True, blank=True, default=json.dumps(obj=[]))
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.recipient.username}: {self.type}"

