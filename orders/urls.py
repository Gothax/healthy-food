from django.urls import path
from . import views
#review
app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('history/', views.order_history, name='order_history'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    
]