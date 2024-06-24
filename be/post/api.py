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
import os
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
from search.api import get_embedding
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

# hugging face model
processor = AutoImageProcessor.from_pretrained("dima806/fruit_vegetable_image_detection")
model = AutoModelForImageClassification.from_pretrained("dima806/fruit_vegetable_image_detection")

# 한국어로 변환할 딕셔너리
label_map = {
    "lemon": "레몬",
    "orange": "오렌지",
    "beetroot": "비트루트",
    "mango": "망고",
    "chilli pepper": "고추",
    "banana": "바나나",
    "cauliflower": "콜리플라워",
    "cucumber": "오이",
    "raddish": "무",
    "grapes": "포도",
    "corn": "옥수수",
    "pomegranate": "석류",
    "bell pepper": "피망",
    "peas": "완두콩",
    "pear": "배",
    "sweetpotato": "고구마",
    "carrot": "당근",
    "capsicum": "고추",
    "spinach": "시금치",
    "apple": "사과",
    "eggplant": "가지",
    "tomato": "토마토",
    "paprika": "파프리카",
    "ginger": "생강",
    "pineapple": "파인애플",
    "garlic": "마늘",
    "soy beans": "대두",
    "watermelon": "수박",
    "cabbage": "양배추",
    "potato": "감자",
    "lettuce": "상추",
    "sweetcorn": "단옥수수",
    "onion": "양파",
    "turnip": "순무",
    "jalepeno": "할라피뇨",
    "kiwi": "키위"
}


class PostListPagination(PageNumberPagination):
    page_size = 6


class ProductListView(ListAPIView):
    queryset = Post.objects.filter(content_type="product")
    serializer_class = PostSerializer
    pagination_class = PostListPagination

    def get_queryset(self):
        queryset = self.queryset
        category_name = self.request.query_params.get('category', 'all')
        trend = self.request.query_params.get('trend', '')

        if category_name != 'all':
            category = get_object_or_404(Category, name=category_name)
            queryset = queryset.filter(product__category=category)

        if trend:
            queryset = queryset.filter(body__icontains='#' + trend)

        return queryset


class PostListView(ListAPIView):
    queryset = Post.objects.filter(content_type__in=['post', 'review'])
    serializer_class = PostDetailSerializer
    pagination_class = PostListPagination

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.annotate(comments_count=Count('comments'))
        return queryset


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
            
        # image로 labe 생성
        first_image = request.FILES.getlist('images')[0]
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        image_path = os.path.join(temp_dir, first_image.name)
        try:
            with open(image_path, 'wb+') as destination:
                for chunk in first_image.chunks():
                    destination.write(chunk)
            
            image = Image.open(image_path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt")
            with torch.no_grad():
                outputs = model(**inputs)
            logits = outputs.logits
            predicted_class_idx = logits.argmax(-1).item()
            label = model.config.id2label[predicted_class_idx]
            korean_label = label_map.get(label, "알 수 없음")
            label_embedding = get_embedding(korean_label)
            
            post.label_embedding = label_embedding
            post.save()


        finally:
            # 임시 파일 삭제
            if os.path.exists(image_path):
                os.remove(image_path)

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


