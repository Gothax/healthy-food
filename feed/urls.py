from django.contrib import admin
from django.urls import path
from . import views
from .views import like_content

app_name='feed'
urlpatterns = [
    path('', views.ContentListView.as_view(), name='index'),
    path('create/post/', views.ContentCreateView.as_view(), name='post-create'),
    path('create/review/', views.ReviewCreateView.as_view(), name='review-create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    path('like/<int:content_id>/', like_content, name='like_content'),
    path('comment/create/<int:pk>/', views.comments_create, name='comments_create'), 
    path('comment/delete/<int:pk>/', views.comments_delete, name='comments_delete'), 
    path('comment/update/<int:pk>/',views.comments_update,name ='comments_update'), #추가1
    path('comment_like/<int:pk>/', views.comment_like, name='comment_like'),#추가2  
    path('user/<int:pk>/', views.view_user, name='view_user'),
    
    ]