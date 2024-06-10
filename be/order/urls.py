from django.urls import path
from . import api

# config path('api/orders/', include('order.urls')),

urlpatterns = [
    path('create/', api.create_order, name='create_order'),
    path('history/', api.order_history, name='order_history'),
    # path('<uuid:pk>/', api.order_detail, name='order_detail'),
]
