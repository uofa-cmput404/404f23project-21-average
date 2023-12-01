from django.test import TestCase #Using Djangos Built in TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import Author,Comment, Post, Follow, Inbox,PostLike, CommentLike
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


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
        self.author = Author.objects.create(username='test_author', github='https://github.com/test_user') # Replace URL with a real user. 

    @patch('requests.get')
    def test_get_github_events(self, mock_requests_get):
        # Test retrieving GitHub events for an author
        mock_response = mock_requests_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{'event_type': 'PushEvent', 'created_at': '2023-01-01T12:00:00Z'}] # Setting up a mock HTTP response for a GitHub API request

        response = self.client.post(reverse('github-events', args=[self.author.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('event_type', response.data[0])
        self.assertIn('created_at', response.data[0])

    @patch('requests.get')
    def test_get_github_events_not_found(self, mock_requests_get):
        # Test handling the case where GitHub events are not found
        mock_response = mock_requests_get.return_value
        mock_response.status_code = 404

        response = self.client.post(reverse('github-events', args=[self.author.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('GitHub not found', response.data['message'])

# Tests for Inbox View

class InboxItemViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a test author
        self.author = Author.objects.create(username='test_author')
        # Create an inbox for the test author
        Inbox.objects.create(author=self.author, items='[]')

    def test_get_inbox_items(self):
        # Test getting inbox items for the current user
        url = reverse('inbox', args=[self.author.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_follow_item_to_inbox(self): #DOUBLE CHECK THIS TEST
        # Test adding a follow item to the inbox
        url = reverse('inbox', args=[self.author.pk])
        follow_item = {
            "type": "follow",
        }
        response = self.client.post(url, {'items': follow_item}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_like_item_to_inbox(self):
        # Test adding a like item to the inbox
        url = reverse('inbox', args=[self.author.pk])
        like_item = {
            "type": "like",
        }
        response = self.client.post(url, {'items': like_item}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_comment_item_to_inbox(self):
        # Test adding a comment item to the inbox
        url = reverse('inbox', args=[self.author.pk])
        comment_item = {
            "type": "comment",
        }
        response = self.client.post(url, {'items': comment_item}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_post_item_to_inbox(self):
        # Test adding a post item to the inbox
        url = reverse('inbox', args=[self.author.pk])
        post_item = {
            "type": "post",
        }
        response = self.client.post(url, {'items': post_item}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_inbox_items(self):
        # Test deleting all inbox items for the current user
        url = reverse('inbox-items', args=[self.author.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# Tests for Likes View

# Tests for Post View

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


# Tests for Share View

class ShareViewTestCase(APITestCase):
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