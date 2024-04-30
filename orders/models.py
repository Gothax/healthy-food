# models.py
from django.db import models
from django.contrib.auth.models import User
from product.models import Product  # Product 모델 import 추가

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=250)
    buyer_name = models.CharField(max_length=250)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
<<<<<<< HEAD
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
=======
    menu = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)  # 수정된 부분
>>>>>>> afe24572985271179b2445ebc3d0733e766aee0c
    quantity = models.IntegerField()

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    seller_name = models.CharField(max_length=250)

    def __str__(self):
        return self.seller_name

class SellerProduct(models.Model):
    name = models.CharField(max_length=250)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
