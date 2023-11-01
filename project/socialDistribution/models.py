from datetime import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
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
    print('25:', instance, end="\n\n")
    if created:
        Author.objects.create(displayName=instance, user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print('32:', sender, instance, kwargs, end="\n\n")
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
