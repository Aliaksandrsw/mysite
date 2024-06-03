from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.models import Post, Comment
from taggit.models import Tag


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )

    def test_post_model(self):
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='This is a test post.',
            status=Post.Status.PUBLISHED
        )
        post.tags.add('tag1', 'tag2')
        self.assertEqual(str(post), 'Test Post')
        self.assertEqual(post.get_absolute_url(), f'/{post.slug}/')
        published_posts = Post.published.all()
        self.assertIn(post, published_posts)

    def test_comment_model(self):
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='This is a test post.',
            status=Post.Status.PUBLISHED
        )
        comment = Comment.objects.create(
            post=post,
            name='John Doe',
            email='john@example.com',
            body='This is a test comment.'
        )
        self.assertEqual(str(comment), 'Comment by John Doe on Test Post')
