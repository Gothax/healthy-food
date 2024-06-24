from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignupForm, ProfileForm
from .models import User
from .serializers import UserSerializer, UserSerializerNoIMG, SalesSerializer
from .permissions import IsSeller
from post.models import Product
from order.models import OrderItem, Order
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Sum, Count, F, Subquery

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'user_image': request.user.get_userimage(),
        'is_seller': request.user.is_seller,
    })

@api_view(['GET'])
def me_noimg(request):
    serializer = UserSerializerNoIMG(request.user)
    return JsonResponse(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()

        # 이메일 확인 로직 추가
    else:
        message = form.errors.as_json()
        
    return JsonResponse({'message': message}, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_follow(request, pk):
    me = request.user
    you = User.objects.get(pk=pk)
    
    if me in you.followers.all(): 
        you.followers.remove(me)
        return JsonResponse({'message': 'unfollow'})
    else:
        you.followers.add(me)
        return JsonResponse({'message': 'follow'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_follow(request, pk):
    me = request.user
    you = User.objects.get(pk=pk)
    
    if me in you.followers.all(): 
        return JsonResponse({'isFollowing': True})
    else:
        return JsonResponse({'isFollowing': False})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editprofile(request):
    user = request.user
    name = request.data.get('name')
    
    if User.objects.exclude(id=user.id).filter(name=name).exists():
        return JsonResponse({'message': 'nickname already exists'})
    
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        serializer = UserSerializer(user)
        
        return JsonResponse({'message': 'information updated', 'user': serializer.data})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editpassword(request):
    user = request.user
    
    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_seller(request):
    user = request.user
    business_number = request.data.get('business_number')

    if not business_number:
        return JsonResponse({'message': 'Business number is required'}, status=400)

    user.is_seller = True
    user.business_number = business_number
    user.save()

    return JsonResponse({'message': 'You have been registered as a seller.'})

@api_view(['GET'])
@permission_classes([IsSeller])
def sales(request):
    seller = request.user
    products = Product.objects.filter(posts__created_by=seller)

    # Order 테이블을 기준으로 월별 주문 수를 카운트
    monthly_orders = (
        Order.objects
        .filter(id__in=Subquery(
            OrderItem.objects
            .filter(product__in=products)
            .values('order_id')
        ))
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total_count=Count('id'))
        .order_by('month')
    )
    
    # 각 월별로 판매 금액 계산
    monthly_sales = (
        OrderItem.objects
        .filter(product__in=products)
        .annotate(month=TruncMonth('order__created_at'))
        .values('month')
        .annotate(total_sales=Sum(F('product__price') * F('quantity')))
        .order_by('month')
        )
    
    # 월별 주문 수와 판매 금액을 합침
    monthly_data = {}
    for order in monthly_orders:
        month = order['month'].date()
        monthly_data[month] = {
            'month': month,
            'total_count': order['total_count'],
            'total_sales': 0
        }
    
    for sale in monthly_sales:
        month = sale['month'].date()
        if month in monthly_data:
            monthly_data[month]['total_sales'] = sale['total_sales']
    
    # 리스트 형태로 변환
    monthly_sales_list = list(monthly_data.values())
    
    # SalesSerializer가 기대하는 형식에 맞게 데이터 전달
    serializer = SalesSerializer(data={'monthly_sales': monthly_sales_list})
    if serializer.is_valid():
        return JsonResponse(serializer.validated_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid data', 'details': serializer.errors}, status=400)
