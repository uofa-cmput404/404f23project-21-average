from django.test import TestCase #Using Djangos Built in TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import Author,Comment, Post, Follow
import requests
from unittest.mock import patch, MagicMock


#Testing for authorView.py

class AuthorViewsTest(TestCase):
    def setUp(self):
        # Set up any necessary test data
        self.client = APIClient()
        # Create a test author
        self.author = Author.objects.create(username='test_author')

    def test_author_list_view(self):
        # Test AuthorListViewSet
        response = self.client.get(reverse('authors-list')) #Reverse creates a URL based on the view name. 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_node_list_view(self):
        # Test NodeListViewSet
        response = self.client.get(reverse('nodes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_author_detail_view(self):
        # Test AuthorDetailView GET
        response = self.client.get(reverse('authors', args=[self.author.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)

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

    
#Tests for CommentView.py

class CommentViewsTest(TestCase):
    def setUp(self):
        # Set up for the Test Data
        self.client = APIClient()
        # Create test author, post, and comment instances
        self.author = Author.objects.create(username='test_author')
        self.post = Post.objects.create(author=self.author, title='Test Post', content='Test Content', visibility='PUBLIC')
        self.comment_data = {'text': 'Test Comment'}

    def test_comment_list_view(self):
        # Test CommentViewSet GET
        response = self.client.get(f'/path/to/comment-list/{self.author.pk}/{self.post.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_comment_create_view(self):
        # Test CommentViewSet POST
        response = self.client.post(f'/path/to/comment-list/{self.author.pk}/{self.post.pk}/', self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #Check for a Text Field:
        self.assertIn('text', response.data)
        self.assertEqual(response.data['text'], self.comment_data['text'])

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