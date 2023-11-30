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