from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post
from django.contrib.auth import get_user_model


class BlogURLsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        User = get_user_model()
        test_user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            body='This is a test post.',
            status=Post.Status.PUBLISHED,
            author=test_user
        )

    def test_post_list_url(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url(self):
        response = self.client.get(reverse('blog:post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)

    def test_post_create_url(self):
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 302)  # Редирект на страницу входа

    def test_post_update_url(self):
        response = self.client.get(reverse('blog:post_update', args=[self.post.slug]))
        self.assertEqual(response.status_code, 302)  # Редирект на страницу входа

    def test_post_list_by_tag_url(self):
        tag = self.post.tags.create(name='Test Tag')
        response = self.client.get(reverse('blog:post_list_by_tag', args=[tag.slug]))
        self.assertEqual(response.status_code, 200)

    def test_post_search_url(self):
        response = self.client.get(reverse('blog:post_search'))
        self.assertEqual(response.status_code, 200)

    def test_post_share_url(self):
        response = self.client.get(reverse('blog:post_share', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_comment_url(self):
        response = self.client.get(reverse('blog:post_comment', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  # Редирект на страницу входа
