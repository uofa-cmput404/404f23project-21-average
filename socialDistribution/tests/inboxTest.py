from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from socialDistribution.models import Author, Inbox
import base64


class InboxItemViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.headers = {'Authorization': f"Basic {base64.b64encode('21average:bigPass'.encode('utf - 8')).decode('utf - 8')}"}
        # Create a test author
        self.author = Author.objects.get(username='string')
        # Create an inbox for the test author
        # Inbox.objects.create(author=self.author, items='[]')

    def test_get_inbox_items(self):
        # Test getting inbox items for the current user
        response = self.client.get(reverse('inbox', kwargs={'author_pk': self.author.id}), headers=self.headers)
        print(response.data, response.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_follow_item_to_inbox(self):  # DOUBLE CHECK THIS TEST
        # Test adding a follow item to the inbox
        
        follow_item = {
            "type": "follow",
        }
        response = self.client.post(reverse('inbox', kwargs={'author_pk': self.author.id}), data={'items': follow_item}, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_like_item_to_inbox(self):
        # Test adding a like item to the inbox
        
        like_item = {
            "type": "like",
        }
        response = self.client.post(reverse('inbox', kwargs={'author_pk': self.author.id}), data={'items': like_item}, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_comment_item_to_inbox(self):
        # Test adding a comment item to the inbox
        
        comment_item = {
            "type": "comment",
        }
        response = self.client.post(reverse('inbox', kwargs={'author_pk': self.author.id}), data={'items': comment_item}, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_post_item_to_inbox(self):
        # Test adding a post item to the inbox
        
        post_item = {
            "type": "post",
        }
        response = self.client.post(reverse('inbox', kwargs={'author_pk': self.author.id}), data={'items': post_item}, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_inbox_items(self):
        # Test deleting all inbox items for the current user
        
        response = self.client.delete(reverse('inbox', kwargs={'author_pk': self.author.id}), headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
