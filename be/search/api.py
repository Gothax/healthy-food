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

    start = time.time()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id
            FROM post_product
            ORDER BY embeddings <=> %s::vector
            LIMIT 10
        """, [query_embedding])
        product_ids = [row[0] for row in cursor.fetchall()]
        
    end = time.time()
    print(f"Search execution time: {end - start} seconds")

    products = Product.objects.filter(id__in=product_ids)

    # products에 해당하는 posts를 추출
    posts = Post.objects.filter(product__in=products)
    posts_serializer = PostSerializer(posts, many=True)

    return JsonResponse({
        'posts': posts_serializer.data
    }, safe=False)