from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    # id = models.CharField(max_length=255, primary_key=True)
    public = models.BooleanField()
    host = models.CharField(max_length=255)
    displayName = models.CharField(max_length=255)
    url = models.TextField()
    github = models.TextField()
    profileImage = models.TextField()
    # One to Many relationship
    posts = models.ForeignKey('Post', on_delete=models.CASCADE)
    # One to Many relationship
    comments = models.ForeignKey('Comment', on_delete=models.CASCADE)
    followers = models.ManyToManyField(
        'self', through="Follow", symmetrical=False)

    def __str__(self):
        return self.displayName


class Post(models.Model):
    type = models.CharField(max_length=255)
    id = models.UUIDField(primary_key=True)
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
    commenter = models.ForeignKey(Author, on_delete=models.CASCADE)
    parentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    comment = models.TextField()
    contentType = models.CharField(max_length=255)
    published = models.DateTimeField()
    id = models.UUIDField(primary_key=True)


class Follow(models.Model):
    from_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='from_author_follow')
    to_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='to_author_follow')
    status = models.CharField(max_length=255)
    id = models.UUIDField(primary_key=True)


class FriendRequest(models.Model):
    from_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='from_author')
    to_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='to_author')
    status = models.CharField(max_length=255)
    id = models.UUIDField(primary_key=True)


class Like(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    published = models.DateTimeField()
    id = models.UUIDField(primary_key=True)


class ConnectedNode(models.Model):
    id = models.UUIDField(primary_key=True)
    url = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    teamName = models.CharField(max_length=255)
