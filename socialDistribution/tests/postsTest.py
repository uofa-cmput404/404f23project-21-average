from datetime import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from ..models import Post, Author
from ..serializers import PostSerializer
import uuid
import base64

# initialize the APIClient app
client = APIClient()
headers = {'Authorization': f"Basic {base64.b64encode('string:string'.encode('utf-8')).decode('utf-8')}"}


class GetAllPostsTest(TestCase):
    """ Test module for GET all posts API """

    def setUp(self):
        # create user
        user_data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(reverse('rest_register'), user_data)

        # authenticate user
        auth_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('rest_login'), auth_data, headers=headers)
        self.authorId = response.data['user']['pk']
        self.token = response.data['access']
        self.header = {'Authorization': 'Basic ' + self.token}

        author = Author.objects.get(pk=self.authorId)

        self.first_post = Post.objects.create(
            title='First Post', content='This is the first post', author=author)

        self.valid_payload = {
            'title': 'First Post',
            'content': 'This is the first post',
            'published': datetime.now(),
        }

    def test_get_all_posts(self):
        # get API response

        header = {'Authorization': 'Bearer ' + self.token}

        response = client.get(
            reverse('posts-list', kwargs={'author_pk': self.authorId}), headers=header)
        # get data from db
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_post(self):
        response = client.get(
            reverse('posts-detail', kwargs={'author_pk': self.authorId,
                                            'post_pk': self.first_post.pk}), headers=headers)
        post = Post.objects.get(pk=self.first_post.pk)
        serializer = PostSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_post(self):
        response = self.client.post(
            reverse('posts-list', kwargs={'author_pk': self.authorId}),
            data=self.valid_payload, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_update_post(self):
        self.update_post = {
            'title': 'Updated Post',
            'content': 'This is the updated post',
            'published': datetime.now(),
        }
        response = self.client.post(
            reverse('posts-detail', kwargs={'author_pk': self.authorId,
                                            'post_pk': self.first_post.pk}),
            data=self.update_post,
            headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create_post_given_id(self):
    #     self.update_post = {
    #         "title": "string",
    #         "source": "string",
    #         "origin": "string",
    #         "description": "string",
    #         "contentType": "string",
    #         "visibility": "string",
    #         "unlisted": False,
    #         "content": "string",
    #         "published": datetime.now(),
    #         "categories": "string",
    #         "image": None,
    #     }
    #     myuuid = uuid.uuid4()
    #     self.header['Content-Disposition'] = 'attachment; filename="c.txt";'
    #     response = self.client.put(
    #         reverse('posts-detail', kwargs={'author_pk': self.authorId,
    #                                         'post_pk': myuuid}),
    #         data=self.update_post,
    #         headers=headers)
    #     # self.assertEqual(response.data['id'], str(myuuid))
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_one_post_given_id(self):
        response = self.client.get(
            reverse('posts-detail', kwargs={'author_pk': self.authorId,
                                            'post_pk': self.first_post.pk}), headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.first_post.title)

    # def test_invalid_update_post(self):
    #     response = client.put(
    #         reverse('posts-detail', kwargs={'pk': self.first_post.pk}),
    #         data=self.invalid_payload,
    #         format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_post(self):
        response = self.client.delete(
            reverse('posts-detail', kwargs={'author_pk': self.authorId,
                                            'post_pk': self.first_post.pk}), headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_post(self):
        myuuid = uuid.uuid4()
        response = self.client.delete(
            reverse('posts-detail', kwargs={'author_pk': self.authorId,
                                            'post_pk': myuuid}), headers=headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_image(self):
        # Test getting an image associated with a post
        post = Post.objects.create(author=self.author, title='Test Image Post', content='Test Content', visibility='PUBLIC')
        response = self.client.get(f'/posts/{post.id}/image/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
