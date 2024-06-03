from django.test import TestCase
from blog.forms import EmailPostForm, CommentForm, SearchForm, PostCreateForm, PostUpdateForm


class FormTestCase(TestCase):
    def test_email_post_form(self):
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'to': 'jane@example.com',
            'comments': 'Hi, this is a test comment.'
        }
        form = EmailPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form(self):
        form_data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'body': 'This is a test comment.'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form(self):
        form_data = {
            'query': 'test'
        }
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_create_form(self):
        # Создаем фиктивный запрос для теста
        request = self.client.request().wsgi_request
        form_data = {
            'title': 'Test Post',
            'tags': 'tag1, tag2',
            'body': 'This is a test post.',
            'status': 'PB'
        }
        form = PostCreateForm(data=form_data, request=request)
        self.assertTrue(form.is_valid())

    def test_post_update_form(self):
        request = self.client.request().wsgi_request
        form_data = {
            'title': 'Updated Test Post',
            'tags': 'tag1, tag2',
            'body': 'This is an updated test post.',
            'status': 'PB',
            'fixed': True
        }
        form = PostUpdateForm(data=form_data, request=request)
        self.assertTrue(form.is_valid())
