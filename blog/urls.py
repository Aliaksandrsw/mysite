from django.urls import path
from . import views
from .views import PostCreateView, PostUpdateView
app_name = 'blog'

urlpatterns = [
    path('search/', views.PostSearch.as_view(), name='post_search'),
    path('', views.PostList.as_view(), name='post_list'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('<slug:post>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('tag/<slug:tag_slug>/',views.PostList.as_view(), name='post_list_by_tag'),

    path('<int:post_id>/share/', views.PostShareView.as_view(), name='post_share'),
    path('<int:post_id>/comment/', views.PostComment.as_view(), name='post_comment'),
]


