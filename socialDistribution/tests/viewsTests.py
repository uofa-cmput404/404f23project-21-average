from django.test import TestCase  # Using Djangos Built in TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import Author, Comment, Post, Follow, Inbox, PostLike, CommentLike
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

    
class PostViewTestCase(APITestCase):

    def setUp(self):
        # Set Up a User for Testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(user=self.user)
        self.post_data = {
            'title': 'Test Post',
            'content': 'Test Content',
            'visibility': 'PUBLIC',
        }

    def test_create_post(self):
        # Test creating a new post
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/authors/{self.author.id}/posts/', data=self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_posts(self):
        # Test getting a list of posts
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/authors/{self.author.id}/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_post(self):
        # Test getting details of a single post
        post = Post.objects.create(author=self.author, title='Test Post', content='Test Content', visibility='PUBLIC')
        response = self.client.get(f'/authors/{self.author.id}/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        # Test updating the details of a post
        post = Post.objects.create(author=self.author, title='Test Post', content='Test Content', visibility='PUBLIC')
        updated_data = {'title': 'Updated Title'}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/authors/{self.author.id}/posts/{post.id}/', data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        # Test deleting a post
        post = Post.objects.create(author=self.author, title='Test Post', content='Test Content', visibility='PUBLIC')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/authors/{self.author.id}/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_image(self):
        # Test getting an image associated with a post
        post = Post.objects.create(author=self.author, title='Test Image Post', content='Test Content', visibility='PUBLIC')
        response = self.client.get(f'/posts/{post.id}/image/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
