from .models import Order

def orders_for_product(product):
    orders = Order.objects.filter(seller=product)
    return orders
