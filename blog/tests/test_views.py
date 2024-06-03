from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from blog.models import Post, Comment
from taggit.models import Tag


class BlogViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user2 = User.objects.create_user(username='author', password='12345')
        self.tag = Tag.objects.create(name='django', slug='django')
        self.post = Post.objects.create(
            title='Test Post',
            body='This is a test post.',
            author=self.user2,
            status=Post.Status.PUBLISHED,
            slug='test-post'
        )
        self.post.tags.add(self.tag)
        self.comment = Comment.objects.create(
            post=self.post,
            name='Test Commenter',
            email='commenter@example.com',
            body='This is a test comment.',
            active=True
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/list.html')
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post_detail',
                                           args=[self.post.publish.year, self.post.publish.month, self.post.publish.day,
                                                 self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/detail.html')
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is a test comment.')

    def test_post_share_view(self):
        response = self.client.post(reverse('blog:post_share', args=[self.post.id]), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'to': 'friend@example.com',
            'comments': 'Check out this post!'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after success

    def test_post_comment_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('blog:add_comment_to_post', args=[self.post.id]), {
            'name': 'New Commenter',
            'email': 'newcommenter@example.com',
            'body': 'This is another test comment.'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertTrue(Comment.objects.filter(body='This is another test comment.').exists())

    def test_post_search_view(self):
        response = self.client.get(reverse('blog:post_search'), {'query': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/search.html')
        self.assertContains(response, 'Test Post')

    def test_post_create_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'New Post',
            'body': 'This is a new post.',
            'tags': 'django'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_post_update_view(self):
        self.client.login(username='author', password='12345')
        response = self.client.post(reverse('blog:post_update', args=[self.post.id]), {
            'title': 'Updated Post Title',
            'body': 'This is the updated post body.',
            'tags': 'django'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after success
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post Title')

    def test_post_list_view_with_tag(self):
        response = self.client.get(reverse('blog:post_list_by_tag', args=[self.tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/list.html')
        self.assertContains(response, 'Test Post')
