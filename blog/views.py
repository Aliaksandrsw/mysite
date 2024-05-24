from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView
from taggit.models import Tag
from blog.forms import EmailPostForm, CommentForm, SearchForm
from blog.models import Post


class PostList(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 2
    paginate_orphans = 0

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['form'] = CommentForm()
        context['comments'] = post.comments.filter(active=True)
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Post,
                                 status=Post.Status.PUBLISHED,
                                 slug=self.kwargs['post'],
                                 publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day']
                                 )


class PostShareView(FormView):
    template_name = 'blog/post/share.html'
    form_class = EmailPostForm

    def get_success_url(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'), status=Post.Status.PUBLISHED)
        return reverse_lazy('blog:post_detail', args=[
            post.publish.year, post.publish.month, post.publish.day, post.slug])

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'), status=Post.Status.PUBLISHED)
        post_url = post.get_absolute_url()
        subject = f"{form.cleaned_data['name']} recommends you read {post.title}"
        message = f"Read {post.title} at {post_url}\n\n"
        message += f"{form.cleaned_data['name']} ({form.cleaned_data['email']}) comments: {form.cleaned_data['comments']}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [form.cleaned_data['to']])
        return super().form_valid(form)


class PostComment(CreateView):
    form_class = CommentForm
    template_name = 'blog/post/comment.html'

    def get_success_url(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'), status=Post.Status.PUBLISHED)
        return reverse_lazy('blog:post_detail', args=[
            post.publish.year, post.publish.month, post.publish.day, post.slug])

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'], status=Post.Status.PUBLISHED)
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return super().form_valid(form)


class PostSearch(View):
    def get(self, request):
        form = SearchForm(request.GET)
        query = None
        results = []
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title', 'body')
            ).filter(search=query)
        return render(request, 'blog/post/search.html', {
            'form': form,
            'query': query,
            'results': results
        })

