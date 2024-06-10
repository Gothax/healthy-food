from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
from .models import Order, OrderItem
from account.models import User
from post.models import Product
from .serializers import OrderSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    order_data = request.data.get('order')
    user_data = order_data.get('user')
    
    required_fields = ['real_name', 'phone_number', 'address', 'detailed_address']
    for field in required_fields:
        if not user_data.get(field):
            return JsonResponse({'message': f'{field}이(가) 누락되었습니다.'}, status=400)
   
    user = User.objects.get(email=user_data['email'])     
    user.real_name = user_data.get('real_name', user.real_name)
    user.phone_number = user_data.get('phone_number', user.phone_number)
    user.address = user_data.get('address', user.address)
    user.detailed_address = user_data.get('detailed_address', user.detailed_address)
    user.save()

    order = Order.objects.create(
        user=user,
        created_at=order_data.get('createdAt')
    )
    
    for item in order_data.get('products'):
        product = Product.objects.get(id=item['id'])
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity']
        )

    return JsonResponse({'message': '주문이 완료되었습니다.'}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    serializer = OrderSerializer(orders, many=True)
    return JsonResponse({'orders': serializer.data}, safe=False)

