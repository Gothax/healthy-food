from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from account.models import User
from account.serializers import UserSerializer
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from .models import Post, Like, Comment, Trend, PostAttachment, Category, Product
from .forms import PostForm
from account.permissions import IsSeller
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from order.models import OrderItem
import json
from django.db import transaction


@api_view(['GET'])
def product_list(request):
    category_name = request.GET.get('category', 'all')
    posts = Post.objects.filter(content_type="product")
    
    if category_name != 'all':
        category = get_object_or_404(Category, name=category_name)
        posts = posts.filter(product__category=category)
    
    trend = request.GET.get('trend', '')
    if trend:
        posts = posts.filter(body__icontains='#' + trend)
        
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.filter(content_type__in=['post', 'review'])
    
    serializer = PostDetailSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.annotate(comments_count=Count('comments')).get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.annotate(posts_count=Count('posts')).get(pk=id)
    posts = Post.objects.filter(created_by_id=id)
    reviews = Post.objects.filter(product__seller_id=id, content_type='review')
    
    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    reviews_serializer = PostSerializer(reviews, many=True)

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        'reviews': reviews_serializer.data
    }, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create(request):
    if not request.FILES.getlist('images'):
        return JsonResponse({'error': '이미지 1개 이상 필요합니다'}, status=400)
    
    form = PostForm(request.POST)
    attachments = []

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        for file in request.FILES.getlist('images'):
            attachment = PostAttachment(image=file, post=post)
            attachment.save()
            attachments.append(attachment)

        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': form.errors})
    
@api_view(['POST'])
@permission_classes([IsSeller])
def create_product(request):
    if not request.FILES.getlist('images'):
        return JsonResponse({'error': '이미지 1개 이상 필요합니다'}, status=400)
    
    category_name = request.POST.get('category')
    price = request.POST.get('price')
    name = request.POST.get('name')
    specific = request.POST.get('specific')
    category, _ = Category.objects.get_or_create(name=category_name)
    

    if not all([category_name, price, name, specific]):
        return JsonResponse({'error': '모든 제품 필드를 입력해야 합니다'}, status=400)
    
    product = Product(category=category, price=price, name=name, specific=specific, seller=request.user)
    product.save()

    post = Post(
        body=request.POST.get('body', ''),
        created_by=request.user,
        content_type='product',
        product=product
    )
    post.save()

    attachments = []
    for file in request.FILES.getlist('images'):
        attachment = PostAttachment(image=file, post=post)
        attachment.save()
        attachments.append(attachment)

    serializer = PostSerializer(post)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):

    if not request.FILES.getlist('images'):
        return JsonResponse({'error': '이미지 1개 이상 필요합니다'}, status=400)
    
    body = request.POST.get('body', '')
    product_data = json.loads(request.POST.get('product', '{}'))
    order_item_data = json.loads(request.POST.get('orderItem', '{}'))

    with transaction.atomic():
        product = Product.objects.get(id=product_data['id'])
        order_item = OrderItem.objects.get(id=order_item_data['id'])
        
        post = Post.objects.create(
            body=body,
            created_by=request.user,
            content_type='review',
            product=product
        )
        post.save()
        
        order_item.review_id = post.id
        order_item.save()
        
        attachments = []
        for file in request.FILES.getlist('images'):
            attachment = PostAttachment(image=file, post=post)
            attachment.save()
            attachments.append(attachment)
        
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_like(request, pk):   
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)
        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        return JsonResponse({'message': 'like created'})
    else:
        like = Like.objects.filter(created_by=request.user, post=pk).first()
        post = Post.objects.get(pk=pk)
        post.likes.remove(like)
        post.likes_count = post.likes_count - 1
        post.save()
        like.delete()

        return JsonResponse({'message': 'like canceled'})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_liked(request, pk):
    post = Post.objects.get(pk=pk)    
    me = request.user
    is_liked = Like.objects.filter(created_by=me, post=post).exists()
    return JsonResponse({'isLiked': is_liked})
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user, post=Post.objects.get(pk=pk))
    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return JsonResponse({'message': 'post deleted'})

@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)


