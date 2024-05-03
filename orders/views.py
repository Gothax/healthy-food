from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required

#review
@login_required
def create_order(request):
    # POST 요청인지 확인
    if request.method == 'POST':
        cart = request.session[settings.CART_ID]
        user = request.user
        
        # 장바구니가 비어있는지 확인
        if not cart:
            return HttpResponse('장바구니가 비어 있습니다.', status=400)
        
        order = Order.objects.create(
            created_at = models.DateTimeField(auto_now_add=True),
            user = user,
            )
        
        for item_id, comp in cart.items():
            quantity = comp['quantity']
            OrderItem.objects.create(
                order_id=order.pk,
                product_id=item_id,
                quantity=quantity
            )

        # 장바구니 비우기 (주문이 완료된 후)
        cart.clear()
        
        return redirect('orders:order_detail', order_id=order.id) 
        
    else:
        # GET 요청 시 에러 메시지 반환
        return HttpResponse('잘못된 요청입니다.', status=405)


@login_required
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user) 
    orders_with_total = []
    for order in orders:
        total_price = order.get_total_price()  # 이전에 정의한 get_total_price 메소드 사용
        orders_with_total.append((order, total_price))
    
    # 템플릿에 orders_with_total 리스트를 전달
    return render(request, 'orders/order_history.html', {'orders_with_total': orders_with_total})


@login_required
def order_detail(request, order_id):
    # 주문 ID를 사용하여 주문 정보를 가져옴
    order = get_object_or_404(Order, id=order_id)

    # 해당 주문에 속한 모든 상품 아이템들을 가져옴
    order_items = OrderItem.objects.filter(order=order)

    # 주문 정보와 상품 아이템들을 템플릿에 전달하여 주문 상세 페이지를 렌더링
    return render(request, 'orders/order_detail.html', {'order': order, 'order_items': order_items})

