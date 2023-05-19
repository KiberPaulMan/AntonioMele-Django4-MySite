from django.urls import path
from . import views

urlpatterns = [
    # path('', views.PostListView.as_view(), name='post_list'),
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('<int:id>', views.post_detail, name='post_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.share_post, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]
