from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('sales_history/', views.sales_history, name='sales_history'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('sales_settlement/', views.sales_settlement, name='sales_settlement'),
    
]