from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # представления поста
    path('', views.PostList.as_view(), name='post_list'),
    path('<int:id>/', views.PostDetail.as_view(), name='post_detail'),
]