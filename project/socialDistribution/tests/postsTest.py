from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Post
from ..serializers import PostSerializer

# initialize the APIClient app
client = APIClient()

class GetAllPostsTest(TestCase):
    """ Test module for GET all posts API """

    def setUp(self):
        Post.objects.create(
            title='First Post', content='This is the first post')
        Post.objects.create(
            title='Second Post', content='This is the second post')

    def test_get_all_posts(self):
        # get API response
        response = client.get(reverse('posts-list'))
        # get data from db
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetSinglePostTest(TestCase):
    """ Test module for GET single post API """

    def setUp(self):
        self.first_post = Post.objects.create(
            title='First Post', content='This is the first post')
        self.second_post = Post.objects.create(
            title='Second Post', content='This is the second post')

    def test_get_valid_single_post(self):
        response = client.get(
            reverse('posts-detail', kwargs={'pk': self.first_post.pk}))
        post = Post.objects.get(pk=self.first_post.pk)
        serializer = PostSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_post(self):
        response = client.get(
            reverse('posts-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewPostTest(TestCase):
    """ Test module for inserting a new post """

    def setUp(self):
        self.valid_payload = {
            'title': 'First Post',
            'content': 'This is the first post'
        }
        self.invalid_payload = {
            'title': '',
            'content': 'This is the first post'
        }

    def test_create_valid_post(self):
        response = client.post(
            reverse('posts-list'),
            data=self.valid_payload,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_post(self):
        response = client.post(
            reverse('posts-list'),
            data=self.invalid_payload,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSinglePostTest(TestCase):
    """ Test module for updating an existing post record """

    def setUp(self):
        self.first_post = Post.objects.create(
            title='First Post', content='This is the first post')
        self.second_post = Post.objects.create(
            title='Second Post', content='This is the second post')
        self.valid_payload = {
            'title': 'Updated Post',
            'content': 'This is the updated post'
        }
        self.invalid_payload = {
            'title': '',
            'content': 'This is the updated post'
        }

    def test_valid_update_post(self):
        response = client.put(
            reverse('posts-detail', kwargs={'pk': self.first_post.pk}),
            data=self.valid_payload,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_post(self):
        response = client.put(
            reverse('posts-detail', kwargs={'pk': self.first_post.pk}),
            data=self.invalid_payload,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSinglePostTest(TestCase):
    """ Test module for deleting an existing post record """

    def setUp(self):
        self.first_post = Post.objects.create(
            title='First Post', content='This is the first post')
        self.second_post = Post.objects.create(
            title='Second Post', content='This is the second post')

    def test_valid_delete_post(self):
        response = client.delete(
            reverse('posts-detail', kwargs={'pk': self.first_post.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_post(self):
        response = client.delete(
            reverse('posts-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)