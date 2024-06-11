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
    products = Product.objects.annotate(
        similarity=CosineDistance(F('embeddings'), query_embedding)
    ).order_by('similarity')[:10]

    posts = Post.objects.filter(product__in=products)
    posts_serializer = PostSerializer(posts, many=True)
    return JsonResponse({
        'posts': posts_serializer.data
    }, safe=False)
    
# @api_view(['POST'])
# def search(request):
#     data = request.data
#     query = data['query']
#     query_embedding = get_embedding(query)
#     products = Product.objects.annotate(
#         similarity=CosineDistance(F('embeddings'), query_embedding)
#     ).order_by('similarity')[:10]

#     users = User.objects.filter(name__icontains=query)
#     users_serializer = UserSerializer(users, many=True)

#     posts = products.posts
#     posts_serializer = PostSerializer(posts, many=True)

#     return JsonResponse({
#         'users': users_serializer.data,
#         'posts': posts_serializer.data
#     }, safe=False)
    
    
#최적화를 위해 추가해야할 설정    
# CREATE INDEX ON products USING hnsw (embeddings vector_cosine_ops);

# @api_view(['POST'])
# def search(request):
#     data = request.data
#     query = data['query']

#     # Get embedding for the query
#     query_embedding = get_embedding(query)

#     # Use raw SQL to leverage the HNSW index for efficient nearest neighbor search
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT id, name, specific
#             FROM products
#             ORDER BY embeddings <=> %s
#             LIMIT 10
#         """, [query_embedding])
#         rows = cursor.fetchall()

#     # Convert the result to a list of dictionaries
#     products = [
#         {'id': row[0], 'name': row[1], 'specific': row[2]}
#         for row in rows
#     ]

#     return JsonResponse({'products': products}, safe=False)


# @api_view(['POST'])
# def search(request):
#     data = request.data
#     query = data['query']
#     query_embedding = get_embedding(query)
#     print(query)
#     print(query_embedding)
    
#     # Use raw SQL to leverage the HNSW index for efficient nearest neighbor search
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT id
#             FROM post_product
#             ORDER BY embeddings <=> %s
#             LIMIT 10
#         """, [query_embedding])
#         product_ids = [row[0] for row in cursor.fetchall()]
    
#     products = Product.objects.filter(id__in=product_ids)
#     print(products)

#     users = User.objects.filter(name__icontains=query)
#     users_serializer = UserSerializer(users, many=True)

#     # products에 해당하는 posts를 추출
#     posts = Post.objects.filter(product__in=products)
#     posts_serializer = PostSerializer(posts, many=True)

#     return JsonResponse({
#         'users': users_serializer.data,
#         'posts': posts_serializer.data
#     }, safe=False)