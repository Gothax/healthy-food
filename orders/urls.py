from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('history/', views.order_history, name='order_history'),
    path('all/', views.all_orders, name='all_orders'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    #  path('product_orders/<int:product_id>/', views.product_orders, name='product_orders'),
    path('seller/<int:seller_id>/purchase-history/', views.seller_purchase_history, name='seller_purchase_history'),
    # 다른 URL 패턴들을 여기에 추가할 수 있습니다.


    # 다른 URL 패턴들을 여기에 추가할 수 있습니다.
]
