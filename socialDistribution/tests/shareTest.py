from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from socialDistribution.models import Author, Inbox, Post, Comment


class ShareViewTestCase(TestCase):

    def setUp(self):
        # Set up a user and author for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(user=self.user)
        # Set up a post for testing
        self.post_data = {
            'title': 'Test Post',
            'content': 'Test Content',
            'visibility': 'PUBLIC',
        }
        self.post = Post.objects.create(author=self.author, **self.post_data)

    def test_share_public_post(self):
        # Test sharing a public post
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/share/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Post shared'})

    def test_share_friends_post(self):
        # Test sharing a friends-only post
        self.post.visibility = 'FRIENDS'
        self.post.save()
        
        friend_user = User.objects.create_user(username='frienduser', password='friendpassword')
        friend_author = Author.objects.create(user=friend_user)
        self.author.friends.add(friend_author)

        self.client.force_authenticate(user=friend_user)
        response = self.client.post(f'/share/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Post shared'})
