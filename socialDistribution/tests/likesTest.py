from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from socialDistribution.models import Author, Inbox, Post, Comment
import base64
from django.urls import reverse


class LikeViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # Set up a user and author for testing
        # self.user = Author.objects.get(username='string')
        self.author = Author.objects.get(username='string')
        self.headers = {'Authorization': f"Basic {base64.b64encode('string:string'.encode('utf-8')).decode('utf-8')}"}
        
        # Set up a test post and comment
        self.post_data = {
            'title': 'Test Post',
            'content': 'Test Content',
            'visibility': 'PUBLIC',
        }
        self.post = Post.objects.create(author=self.author, **self.post_data)

        self.comment_data = {
            "type": "comment",
            "comment": "comment",
            "contentType": 'text/plain',
        }
        self.comment = Comment.objects.create(author=self.author, post=self.post, **self.comment_data)

    def test_add_like_to_post_view(self):
        # Test AddLikeToPostView
        response = self.client.post(reverse('post-likes', kwargs={'author_pk': self.author.id, 'post_pk': self.post.id}), headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_like_to_comment_view(self):
        # Test AddLikeToCommentView
        response = self.client.post(reverse('comment-likes',
        kwargs={'author_pk': self.author.id, 'post_pk': self.post.id, 'comment_pk': self.comment.id}),
        headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_author_likes_view(self):
        # Test GetAllAuthorLikes
        response = self.client.get(reverse('liked-posts', kwargs={'author_pk': self.author.id}), headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
