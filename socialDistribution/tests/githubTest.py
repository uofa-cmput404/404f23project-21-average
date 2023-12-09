from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from socialDistribution.models import Author
import base64


class GitHubViewTest(TestCase):

    def setUp(self):
        # Set up any necessary test data
        self.client = APIClient()
        self.header = {'Authorization':
        f"Basic {base64.b64encode('string:string'.encode('utf-8')).decode('utf-8')}"}
        # Create a test author with a GitHub username
        self.author = Author.objects.create(username='test_author', github='https://github.com/AfaqNabi')  # Replace URL with a real user. 

    def test_get_github_events(self):
        # Test retrieving GitHub events for an author
        # mock_response = mock_requests_get.return_value
        # mock_response.status_code = 200
        # mock_response.json.return_value = [{'event_type': 'PushEvent', 'created_at': '2023-01-01T12:00:00Z'}]  # Setting up a mock HTTP response for a GitHub API request

        response = self.client.post(reverse('github', args=[self.author.pk]), headers=self.header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('login', response.data[0])
        self.assertIn('id', response.data[0])

