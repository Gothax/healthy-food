from rest_framework import serializers
from .models import Order, OrderItem
from post.models import Product
from post.serializers import ProductSerializer, PostSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    review = PostSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'get_total_item_price', 'review']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'order_items', 'get_total_price']

