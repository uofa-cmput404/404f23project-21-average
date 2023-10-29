from django.test import TestCase, Client
from django.urls import reverse
from ..models import Author, Post, Comment, Like

class LikeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name='John Doe', email='johndoe@example.com')
        self.post = Post.objects.create(title='Test Post', content='This is a test post', author=self.author)
        self.comment = Comment.objects.create(post=self.post, author=self.author, content='This is a test comment')

    def test_like_post(self):
        response = self.client.post(reverse('like_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(post=self.post, author=self.author).exists())

    def test_unlike_post(self):
        like = Like.objects.create(post=self.post, author=self.author)
        response = self.client.post(reverse('unlike_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Like.objects.filter(pk=like.pk).exists())

    def test_like_comment(self):
        response = self.client.post(reverse('like_comment', args=[self.comment.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(comment=self.comment, author=self.author).exists())

    def test_unlike_comment(self):
        like = Like.objects.create(comment=self.comment, author=self.author)
        response = self.client.post(reverse('unlike_comment', args=[self.comment.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Like.objects.filter(pk=like.pk).exists())