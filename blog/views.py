from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from blog.models import Post


class PostList(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 2
    paginate_orphans = 0

    def get_queryset(self):
        return Post.published.all()


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Post.published.all(),
                                 id=self.kwargs['id'])
