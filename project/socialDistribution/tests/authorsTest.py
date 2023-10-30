from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
# from ..models import Author
from ..models import *


class AuthorTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(
            username='John Doe', email='johndoe@example.com')

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

        # check author was created
        author = Author.objects.get(username='testuser')
        self.assertEqual(author.email, 'test@test.com')

    def test_author_list(self):
        response = self.client.get(reverse('authors-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.username)

    def test_author_detail(self):
        response = self.client.get(
            reverse('authors', args=[self.author.pk]))
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
        response = self.client.post(reverse('rest_register'), user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # authenticate user
        auth_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('rest_login'), auth_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        header = {'Authorization': 'Bearer ' + token}

        data = {'host': 'asdasd', 'username': 'JohnSmith', 'displayName': 'testtt', 'github': 'asdasd',
                'email': 'johnsmith@example.com', 'password': 'testts'}
        response = self.client.post(
            reverse('authors', args=[self.author.pk]), data, **header)
        self.assertEqual(response.status_code, 200)
        self.author.refresh_from_db()
        self.assertEqual(self.author.username, 'JohnSmith')
        self.assertEqual(self.author.email, 'johnsmith@example.com')

# def test_author_delete(self):
#     response = self.client.post(
#         reverse('author_delete', args=[self.author.pk]))
#     self.assertEqual(response.status_code, 302)
#     self.assertFalse(Author.objects.filter(pk=self.author.pk).exists())
