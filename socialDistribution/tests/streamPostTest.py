from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from socialDistribution.models import Author, Inbox, Post, Comment
from django.contrib.auth.models import User
from django.test import TestCase


class StreamPostListTestCase(TestCase):

    def setUp(self):
        # Set up a user and author for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(user=self.user)
        
        # Set Up Test Post
        self.post_data = {
            'title': 'Test Post',
            'content': 'Test Content',
            'visibility': 'PUBLIC',
        }
        self.post = Post.objects.create(author=self.author, **self.post_data)

    def test_get_stream_posts(self):
        # Test getting stream posts
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/authors/{self.author.id}/posts/allposts/stream/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_stream_posts_with_friends(self):
        # Test getting stream posts with friends
        friend_user = User.objects.create_user(username='frienduser', password='friendpassword')
        friend_author = Author.objects.create(user=friend_user)
        self.author.friends.add(friend_author)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/authors/{self.author.id}/posts/allposts/stream/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
