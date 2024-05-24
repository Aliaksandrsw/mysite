from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/',views.PostList.as_view(), name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.PostDetail.as_view(), name='post_detail'),
    path('<int:post_id>/share/', views.PostShareView.as_view(), name='post_share'),
    path('<int:post_id>/comment/', views.PostComment.as_view(), name='post_comment'),
    path('search/', views.PostSearch.as_view(), name='post_search'),
]
