from django.test import TestCase #Using Djangos Built in TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import Author

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