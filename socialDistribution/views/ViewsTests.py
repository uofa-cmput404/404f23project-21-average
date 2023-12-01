from django.test import TestCase #Using Djangos Built in TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import Author,Comment, Post, Follow
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta


#Testing for authorView.py

class AuthorViewsTest(TestCase):
    def setUp(self):
        # Set up any necessary test data
        self.client = APIClient()
        # Create a test author
        self.author = Author.objects.create(username='test_author')

    def test_author_list_view(self):
        # Test AuthorListViewSet
        response = self.client.get(reverse('authors-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        # Ensure that the response contains the expected key 'results'

    def test_node_list_view(self):
        # Test NodeListViewSet
        response = self.client.get(reverse('nodes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        # Ensure that the response contains the expected key 'results'

    def test_author_detail_view(self):
        # Test AuthorDetailView GET
        response = self.client.get(reverse('authors', args=[self.author.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)
        # Ensure that the response contains the author's username

    def test_author_detail_view_post(self):
        # Test AuthorDetailView POST
        updated_username = 'Test_user'
        data = {'username': updated_username}
        response = self.client.post(reverse('authors', args=[self.author.pk]), data, format='json')
        # Check if the response is successful HTTP 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the returned data contains the updated username
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], updated_username)

    def test_author_detail_view_delete(self):
        # Test AuthorDetailView DELETE
        response = self.client.delete(reverse('authors', args=[self.author.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure that the response indicates successful deletion with HTTP 204


    
#Tests for CommentView.py

class CommentViewsTest(TestCase):
    def setUp(self):
        # Set up any necessary test data
        self.client = APIClient()
        # Create a test author and post
        self.author = Author.objects.create(username='test_author')
        self.post = Post.objects.create(
            title='Test Post',
            description='Test Description',
            content='Test Content',
            author=self.author
        )
        # Create test data for a comment
        self.comment_data = {
            'comment': 'Test Comment',
            'contentType': 'text/plain',
            'published': (datetime.now() - timedelta(days=1)).isoformat(),
        }

    def test_get_comments_list(self):
        # Test retrieving the list of local comments for a post
        response = self.client.get(reverse('comments', args=[self.author.pk, self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    
    def test_get_comments_list_remote(self):
        # Test retrieving the list of remote comments for a post
        # Remote teams already configured
        response = self.client.get(reverse('comments', args=[self.author.pk, self.post.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_post_comment(self):
        # Test creating a new comment on a post
        response = self.client.post(reverse('comments', args=[self.author.pk, self.post.pk]), self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('comment', response.data)
        self.assertEqual(response.data['comment'], self.comment_data['comment'])

# Tests for followerView.py

class FollowViewsTest(TestCase):
    def setUp(self):
        # Set up any necessary test data
        self.client = APIClient()
        # Create test authors
        self.author1 = Author.objects.create(username='follower_user')
        self.author2 = Author.objects.create(username='followed_user')

    def test_get_followers_list(self):
        # Test retrieving the list of followers for an author
        response = self.client.get(reverse('followers', args=[self.author2.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_get_following_list(self):
        # Test retrieving the list of authors that an author is following
        response = self.client.get(reverse('following', args=[self.author1.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_check_follower_status(self):
        # Test checking if an author is a follower of another author
        response = self.client.get(reverse('check-follow', args=[self.author1.pk, self.author2.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)

    def test_unfollow_author(self):
        # Test unfollowing another author
        follow = Follow.objects.create(following=self.author2, follower=self.author1, status='Accepted')
        response = self.client.delete(reverse('unfollow', args=[self.author1.pk, self.author2.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Follow.objects.filter(following=self.author2, follower=self.author1).exists())

    def test_send_follow_request(self):
        # Test sending a follow request to another author
        response = self.client.put(reverse('follow-request', args=[self.author1.pk, self.author2.pk]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Follow Request Sent Successfully')

    def test_accept_follow_request(self):
        # Test accepting a follow request from another author
        follow_request = Follow.objects.create(following=self.author1, follower=self.author2, status='Pending')
        response = self.client.post(reverse('accept-follow', args=[self.author2.pk, self.author1.pk]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Follow Request Accepted Successfully')

# Tests for Github View

class GitHubViewTest(TestCase):
    def setUp(self):
        # Set up any necessary test data
        self.client = APIClient()
        # Create a test author with a GitHub username
        self.author = Author.objects.create(username='test_author', github='https://github.com/test_user') #Replace URL with a real user. 