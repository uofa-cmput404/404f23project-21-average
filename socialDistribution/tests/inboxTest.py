from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from socialDistribution.models import Author, Inbox


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

    def test_add_follow_item_to_inbox(self):  # DOUBLE CHECK THIS TEST
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
