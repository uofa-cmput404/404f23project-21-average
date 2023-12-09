from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from socialDistribution.models import Author, Post
from datetime import datetime, timedelta
import base64


class CommentViewsTest(TestCase):

    def setUp(self):
        # Set up any necessary test data
        self.client = APIClient()
        user_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(reverse('rest_register'), user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.headers = {'Authorization': f"Basic {base64.b64encode('string:string'.encode('utf - 8')).decode('utf - 8')}"}
        # Create a test author and post
        self.author = Author.objects.get(username='string')
        self.post = Post.objects.filter(author=self.author)[0]

        # Create test data for a comment
        self.comment_data = {
            'comment': 'Test Comment',
            'contentType': 'text/plain',
            'published': (datetime.now() - timedelta(days=1)).isoformat(),
        }

    def test_post_comment(self):
        # Test creating a new comment on a post
        response = self.client.post(reverse('comments', args=[self.author.pk, self.post.pk]), self.comment_data, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('comment', response.data)
        self.assertEqual(response.data['comment'], self.comment_data['comment'])
        
    def test_get_comments_list(self):
        # Test retrieving the list of local comments for a post
        response = self.client.get(reverse('comments', args=[self.author.pk, self.post.pk]), headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('items', response.data)
    
