from rest_framework import generics, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination

from blog.models import Post
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPagination


class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = PostSerializer
