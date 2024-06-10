from django.db import models
from post.models import Product, Post
from account.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
    
    def get_total_price(self):
        return sum(item.get_total_item_price() for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    review = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}" if self.product else "Product not available"
    
    def get_total_item_price(self):
        if self.product:
            return self.quantity * self.product.price
        return 0