import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public = models.BooleanField()
    host = models.CharField(max_length=255)
    displayName = models.CharField(max_length=255)
    url = models.TextField()
    github = models.TextField()
    profileImage = models.TextField()
    # One to Many relationship
    posts = models.ForeignKey('Post', blank=True,
                              null=True, on_delete=models.CASCADE)
    # One to Many relationship
    comments = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, blank=True, null=True)
    followers = models.ManyToManyField(
        'self', through="Follow", symmetrical=False, blank=True, null=True)

    def __str__(self):
        return self.displayName


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.TextField()
    source = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    description = models.TextField()
    contentType = models.CharField(max_length=255)
    content = models.TextField()
    published = models.DateTimeField()
    owner = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.TextField()
    count = models.IntegerField()


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commenter = models.ForeignKey(Author, on_delete=models.CASCADE)
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    contentType = models.CharField(max_length=255)
    published = models.DateTimeField()


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


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    published = models.DateTimeField()


class ConnectedNode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    teamName = models.CharField(max_length=255)
