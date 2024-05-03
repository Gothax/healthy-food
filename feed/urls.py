from django.contrib import admin
from django.urls import path
from . import views
from .views import like_content, post_delete

app_name='feed'
urlpatterns = [
    path('', views.ContentListView.as_view(), name='index'),
    path('create/post/', views.ContentCreateView.as_view(), name='post-create'),
    path('create/review/', views.ReviewCreateView.as_view(), name='review-create'),
    path('path_to_add_product_info_to_session_view', views.add_product_info_to_session, name='add_product_info_to_session'),

    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    path('like-content/<int:content_id>/', like_content, name='like-content'),

    path('comment/create/<int:pk>/', views.comments_create, name='comments_create'), 
    path('comment/delete/<int:pk>/', views.comments_delete, name='comments_delete'), 
    path('user/<int:pk>/', views.view_user, name='view_user'),

    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/delete/<int:pk>/', post_delete, name='post_delete'),

    ]