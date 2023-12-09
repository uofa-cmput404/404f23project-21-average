from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from socialDistribution.models import Author, Inbox, Post, Comment


class LikeViewTests(TestCase):

    def setUp(self):
        # Set up a user and author for testing
        self.user = Author.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(user=self.user)
        
        # Set up a test post and comment
        self.post_data = {
            'title': 'Test Post',
            'content': 'Test Content',
            'visibility': 'PUBLIC',
        }
        self.post = Post.objects.create(author=self.author, **self.post_data)

        self.comment_data = {
            'comment': 'Test Comment',
            'content_type': 'text/plain',
        }
        self.comment = Comment.objects.create(author=self.author, post=self.post, **self.comment_data)

    def test_add_like_to_post_view(self):
        # Test AddLikeToPostView
        response = self.client.post(f'/authors/{self.author.id}/posts/{self.post.id}/likes/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_like_to_comment_view(self):
        # Test AddLikeToCommentView
        response = self.client.post(f'/authors/{self.author.id}/posts/{self.post.id}/comments/{self.comment.id}/likes/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_author_likes_view(self):
        # Test GetAllAuthorLikes
        response = self.client.get(f'/posts/{self.author.id}/liked/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
