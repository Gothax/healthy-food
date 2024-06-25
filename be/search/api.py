from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer
from pgvector.django import CosineDistance
from decouple import config
import requests
from post.models import Product
from post.serializers import ProductSerializer
from django.db.models import F
from django.db import connection
import time

OPENAI_API_KEY = config('OPENAI_API_KEY')

def get_embedding(text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}',
    }
    data = {
        "input": text,
        "model": "text-embedding-3-small"
    }
    response = requests.post('https://api.openai.com/v1/embeddings', headers=headers, json=data)
    response_data = response.json()
    return response_data['data'][0]['embedding']


@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query']
    query_embedding = get_embedding(query)
    similarity_threshold = 0.3  # 유사도 임계값 설정

    # Product 검색
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id
            FROM post_product
            WHERE (1 - (embeddings <=> %s::vector)) >= %s
            ORDER BY embeddings <=> %s::vector
            LIMIT 10
        """, [query_embedding, similarity_threshold, query_embedding])
        product_ids = [row[0] for row in cursor.fetchall()]

    products = Product.objects.filter(id__in=product_ids)

    # products에 해당하는 posts를 추출
    posts_from_products = Post.objects.filter(product__in=products)
    posts_from_products_serializer = PostSerializer(posts_from_products, many=True)

    # Post 검색 (label_embedding 사용, product가 없는 경우만)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id
            FROM post_post
            WHERE product_id IS NULL AND (1 - (label_embedding <=> %s::vector)) >= %s
            ORDER BY label_embedding <=> %s::vector
            LIMIT 10
        """, [query_embedding, similarity_threshold, query_embedding])
        post_ids = [row[0] for row in cursor.fetchall()]

    posts_from_labels = Post.objects.filter(id__in=post_ids)
    posts_from_labels_serializer = PostSerializer(posts_from_labels, many=True)

    return JsonResponse({
        'posts_from_products': posts_from_products_serializer.data,
        'posts_from_labels': posts_from_labels_serializer.data
    }, safe=False)