from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from itertools import groupby
from operator import attrgetter
from cart.cart import Cart
from django.db.models import Sum, F, Count
from django.db.models.functions import TruncMonth

@login_required
def create_order(request):
    # POST 요청인지 확인
    if request.method == 'POST':
        cart = Cart(request)
        user = request.user
        
        # 장바구니가 비어있는지 확인
        if not cart:
            return HttpResponse('장바구니가 비어 있습니다.', status=400)
        
        order = Order.objects.create(
            user=user,
        )
        
        for item in cart:  
            OrderItem.objects.create(
                order=order,
                product=item['product'],  
                quantity=item['quantity'],
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
def sales_history(request):
    # order_id에 따라 그룹화하기 위해 정렬
    sold_items = OrderItem.objects.filter(product__seller=request.user).order_by('order_id').select_related('order', 'product')
    # 각 그룹은 동일한 order_id를 가진 OrderItem들의 리스트
    grouped_sold_items = [list(group) for key, group in groupby(sold_items, key=attrgetter('order_id'))]
    groups_with_total = []
    for group in grouped_sold_items:
        total_price = 0
        for item in group:
            item_total_price = item.get_total_item_price()  # 이전에 정의한 get_total_item_price 메소드 사용
            total_price += item_total_price
        groups_with_total.append((group, total_price))
    return render(request, 'orders/sales_history.html', {'groups_with_total': groups_with_total})

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64
@login_required
def sales_settlement(request):
    # Order 모델에서 created_at 필드를 기준으로 월별로 그룹화하고, 각 그룹의 총 주문 금액을 계산
    monthly_orders = Order.objects.filter(user=request.user).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total_sales=Count('id'),
        total_price=Sum(F('order_items__quantity') * F('order_items__product__price'))
    ).order_by('month')

    # 누적 매출액 계산
    cumulative_total_price = 0
    for order in monthly_orders:
        cumulative_total_price += order['total_price']


    # ApexCharts 이용해 그래프 그리기(쿼리셋을 json 형태로 반환) ***페이지에 출력 안됨 
    # # monthly_orders QuerySet을 JSON으로 직렬화
    # monthly_orders_json = json.dumps(list(monthly_orders), cls=DjangoJSONEncoder)
    # # XSS 공격 방지를 위해 mark_safe 사용
    # monthly_orders_json_safe = mark_safe(monthly_orders_json)

    # matplot 이용해 라인바 차트 이미지 생성하여 html에 전달   ***새로고침 하면 RuntimeError 발생
    # # 월별 매출과 누적 매출을 계산합니다.
    # months = [order['month'].strftime("%Y-%m") for order in monthly_orders]
    # monthly_sales = [order['total_price'] for order in monthly_orders]
    # cumulative_sales = [sum(monthly_sales[:i+1]) for i in range(len(monthly_sales))]
    
    # # Matplotlib을 사용하여 바 차트와 라인 차트를 하나의 그래프에 그립니다.
    # fig, ax1 = plt.subplots()
    
    # # 월별 매출 바 차트
    # ax1.bar(months, monthly_sales, color='b', label='Monthly Sales')
    # ax1.set_xlabel('Month')
    # ax1.set_ylabel('Monthly Sales')
    # ax1.tick_params('y')
    
    # # 누적 매출 라인 차트
    # ax2 = ax1.twinx()
    # ax2.plot(months, cumulative_sales, color='r', label='Cumulative Sales')
    # ax2.set_ylabel('Cumulative Sales', color='r')
    # ax2.tick_params('y')
    
    # fig.tight_layout()
    # plt.xticks(rotation=45)
    # plt.legend()
    
    # # 그래프를 이미지로 변환합니다.
    # buffer = BytesIO()
    # plt.savefig(buffer, format='png')
    # plt.close(fig)
    # buffer.seek(0)
    # image_png = buffer.getvalue()
    # graph = base64.b64encode(image_png)
    # graph = graph.decode('utf-8')
    # buffer.close()

    context = {
        'monthly_orders': monthly_orders,
        'cumulative_total_price': cumulative_total_price,
        # 'graph': graph,
        # 'monthly_orders_json': monthly_orders_json_safe,
    }
    return render(request, "orders/sales_settlement.html", context)

@login_required
def order_detail(request, order_id):
    # 주문 ID를 사용하여 주문 정보를 가져옴
    order = get_object_or_404(Order, id=order_id)

    # 해당 주문에 속한 모든 상품 아이템들을 가져옴
    order_items = OrderItem.objects.filter(order=order)

    # 주문 정보와 상품 아이템들을 템플릿에 전달하여 주문 상세 페이지를 렌더링
    return render(request, 'orders/order_detail.html', {'order': order, 'order_items': order_items})

