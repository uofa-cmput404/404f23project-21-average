from django.test import TestCase, Client
from django.urls import reverse
from ..models import Author

class AuthorTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name='John Doe', email='johndoe@example.com')

    def test_author_list(self):
        response = self.client.get(reverse('author_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.name)

    def test_author_detail(self):
        response = self.client.get(reverse('author_detail', args=[self.author.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.name)
        self.assertContains(response, self.author.email)

    def test_author_create(self):
        data = {'name': 'Jane Doe', 'email': 'janedoe@example.com'}
        response = self.client.post(reverse('author_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Author.objects.filter(name='Jane Doe').exists())

    def test_author_update(self):
        data = {'name': 'John Smith', 'email': 'johnsmith@example.com'}
        response = self.client.post(reverse('author_update', args=[self.author.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.author.refresh_from_db()
        self.assertEqual(self.author.name, 'John Smith')
        self.assertEqual(self.author.email, 'johnsmith@example.com')

    def test_author_delete(self):
        response = self.client.post(reverse('author_delete', args=[self.author.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Author.objects.filter(pk=self.author.pk).exists())

