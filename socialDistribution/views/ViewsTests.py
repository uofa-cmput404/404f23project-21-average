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
class FollowerViewsTest(TestCase):
    def setUp(self):
        # Set up the Test Data
        self.client = APIClient()
        # Create test authors
        self.author1 = Author.objects.create(username='author1')
        self.author2 = Author.objects.create(username='author2')
        # Create test follow relationship
        Follow.objects.create(following=self.author1, follower=self.author2, status="Accepted")

    def test_follow_list_view(self):
        # Test FollowViewSet GET
        response = self.client.get(f'/path/to/follow-list/{self.author1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_follow_detail_view_get(self):
        # Test FollowDetailViewSet GET
        response = self.client.get(f'/path/to/follow-detail/{self.author1.pk}/{self.author2.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, True)

    def test_follow_detail_view_delete(self):
        # Test FollowDetailViewSet DELETE
        response = self.client.delete(f'/path/to/follow-detail/{self.author1.pk}/{self.author2.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_follow_detail_view_put(self):
        # Test FollowDetailViewSet PUT
        response = self.client.put(f'/path/to/follow-detail/{self.author1.pk}/{self.author2.pk}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_follow_detail_view_post(self):
        # Test FollowDetailViewSet POST
        response = self.client.post(f'/path/to/follow-detail/{self.author1.pk}/{self.author2.pk}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
