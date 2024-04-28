from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, Seller, SellerProduct  # SellerProduct 모델 추가
from product.models import Product
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

@login_required
def create_order(request):
    cart = Cart(request)

    if request.method == 'POST':
        address = request.POST.get('address')
        user = request.user
        user_name = user.username
        order = Order.objects.create(user=user, address=address, buyer_name=user_name)
        
        for item_id, item_data in cart.cart.items():
            product_id = item_id
            quantity = item_data['quantity']
            product = get_object_or_404(Product, pk=product_id)
            seller = product.seller

            # 판매자가 이미 존재하는지 확인
            existing_seller = Seller.objects.filter(user=seller).first()
            if not existing_seller:
                # 존재하지 않는다면 새로운 판매자 생성
                new_seller = Seller.objects.create(user=seller, seller_name=seller.username)
                existing_seller = new_seller

            # OrderItem 생성
            order_item = OrderItem.objects.create(order=order, menu=product, quantity=quantity)

            # SellerProduct에 상품 등록
            seller_product, created = SellerProduct.objects.get_or_create(name=product.name, seller=existing_seller)
            if created:
                # 새로 생성된 경우에만 추가
                seller_product.save()
            
        cart.clear()
        return redirect('orders:order_detail', order_id=order.id) 
    elif request.method == 'GET':
        return render(request, 'orders/create_order.html', {'cart': cart})

    
@login_required
def order_detail(request, order_id):
    # 주문 ID를 사용하여 주문 정보를 가져옴
    order = get_object_or_404(Order, id=order_id)

    # 해당 주문에 속한 모든 상품 아이템들을 가져옴
    order_items = OrderItem.objects.filter(order=order)

    # 주문 정보와 상품 아이템들을 템플릿에 전달하여 주문 상세 페이지를 렌더링
    return render(request, 'orders/order_detail.html', {'order': order, 'order_items': order_items})
@login_required
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user)  # user 필드로 변경
    return render(request, 'orders/order_history.html', {'orders': orders})

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def all_orders(request):
    orders = Order.objects.all()
    return render(request, 'orders/all_orders.html', {'orders': orders})
    

from django.shortcuts import render

@login_required
def seller_purchase_history(request, seller_id):
    # 판매자 정보를 가져옵니다.
    seller = get_object_or_404(Seller, pk=seller_id)
    
    # 판매자의 사용자 정보를 가져옵니다.
    user = seller.user
    
    # 판매자가 등록한 상품에 대한 구매 내역을 필터링합니다.
    order_items = OrderItem.objects.filter(menu__seller=user)
    
    # 필요한 정보를 추출하여 딕셔너리에 저장합니다.
    purchase_history = []
    for item in order_items:
        purchase_history.append({
            'seller_name': seller.seller_name,
            'buyer_name': item.order.buyer_name,
            'product_name': item.menu.name,
            'purchase_date': item.order.created_at
        })
    
    # 템플릿에 필요한 정보를 전달합니다.
    context = {
        'seller': seller,
        'purchase_history': purchase_history
    }
    return render(request, 'orders/seller_purchase_history.html', context)
