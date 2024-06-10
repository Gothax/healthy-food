from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignupForm, ProfileForm
from .models import User
from .serializers import UserSerializer, UserSerializerNoIMG

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'user_image': request.user.get_userimage(),
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