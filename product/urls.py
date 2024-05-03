from django.contrib import admin
from django.urls import path
from . import views

#review
app_name='product'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<int:category_id>/', views.ProductListView.as_view(), name='product_by_category'),
    path("product_detail/<int:pk>/", views.product_detail, name='product_detail'),
    
    path('seller', views.seller_index, name='seller_index'),
    path('seller/add_product/', views.add_product, name='add_product'),
    path("product_delete/<int:pk>/", views.product_delete, name='product_delete'),
]
