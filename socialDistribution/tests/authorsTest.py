from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from socialDistribution.models import Author
import base64


class AuthorTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            username='JohnDoe', email='johndoe@example.com', password='test1234')
        self.headers = {'Authorization':
        f"Basic {base64.b64encode('string:string'.encode('utf-8')).decode('utf-8')}"}

    def test_create_author_with_authentication(self):
        # create user
        user_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(reverse('rest_register'), user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # authenticate user
        auth_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('rest_login'), auth_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_list(self):
        response = self.client.get(reverse('authors-list'), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.username)

    def test_author_detail(self):
        response = self.client.get(
            reverse('authors', args=[self.author.pk]), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.username)
        self.assertContains(response, self.author.email)

    def test_author_update(self):
        user_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(reverse('rest_register'), user_data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # authenticate user
        auth_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('rest_login'), auth_data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        header = {'Authorization': 'Bearer ' + token}

        data = {'host': 'asdasd', 'username': 'JohnSmith', 'displayName': 'testtt', 'github': 'asdasd',
                'email': 'johnsmith@example.com', 'password': 'testts'}
        response = self.client.post(
            reverse('authors', args=[self.author.pk]), data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.author.refresh_from_db()
        self.assertEqual(self.author.username, 'JohnSmith')
        self.assertEqual(self.author.email, 'johnsmith@example.com')
    
    def test_node_list_view(self):
        # Test NodeListViewSet
        response = self.client.get(reverse('nodes'), headers=self.headers)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('items', response.data)
        # Ensure that the response contains the expected key 'results'

