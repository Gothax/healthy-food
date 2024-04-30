from django.contrib import admin
from django.urls import path
from . import views

app_name='feed'
urlpatterns = [
    path('', views.ContentListView.as_view(), name='index'),
    path('create/post/', views.ContentCreateView.as_view(), name='post-create'),
    path('create/review/', views.ReviewCreateView.as_view(), name='review-create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('comment/create/<int:pk>/', views.comments_create, name='comments_create'), #추가1
    ]
