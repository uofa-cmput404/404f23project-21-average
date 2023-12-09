from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from socialDistribution.models import Author, Follow
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
