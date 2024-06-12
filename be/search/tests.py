from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import json
from account.models import User
from post.models import Post, Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile
import time
from django.db import connection


import unittest

class SearchPerformanceTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('search')
        self.user = User.objects.get(name='testuser')
        self.client.login(name='testuser', password='testpassword')
        self.category = Category.objects.get(name='fruit')
        
    def test_search_performance(self):
        data = {
            'query': 'test query'
        }
        
        times = []
        for _ in range(10):
            start_time = time.time()
            response = self.client.post(self.url, data, format='json')
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = sum(times) / len(times)
        
        self.assertEqual(response.status_code, 200)
        print(f"Average search execution time: {avg_time} seconds")


# class SearchPerformanceTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('search')
#         self.user = User.objects.create_user(name='testuser', email='testuser@example.com', password='testpassword')
#         self.client.login(name='testuser', password='testpassword')
#         self.category = Category.objects.create(id=1, name='TestCategory')

#     def create_products(self, count):
#         for i in range(count):
#             Product.objects.create(
#                 category=self.category,
#                 price=100,
#                 name=f'TestProduct{i}',
#                 specific='TestSpecific',
#                 seller=self.user,
#                 embeddings=[0.01] * 1536 
#             )

#     def test_search_performance_1000(self):
#         self.create_products(1000)
#         self._test_search_performance()

#     def _test_search_performance(self):
#         data = {
#             'query': 'test query'
#         }
        
#         times = []
#         for _ in range(5):  # 5번 반복하여 평균 시간 계산
#             start_time = time.time()
#             response = self.client.post(self.url, data, format='json')
#             end_time = time.time()
#             times.append(end_time - start_time)
        
#         avg_time = sum(times) / len(times)
        
#         self.assertEqual(response.status_code, 200)
#         print(f"Average search execution time with {Product.objects.count()} products: {avg_time} seconds")
        
        
# class SearchPerformanceTestCaseHNSW(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('search')
#         self.user = User.objects.create_user(name='testuser', email='testuser@example.com', password='testpassword')
#         self.client.login(name='testuser', password='testpassword')
#         self.category = Category.objects.create(id=1, name='TestCategory')
        
#         self.create_hnsw_index()

#     def create_products(self, count):
#         for i in range(count):
#             Product.objects.create(
#                 category=self.category,
#                 price=100,
#                 name=f'TestProduct{i}',
#                 specific='TestSpecific',
#                 seller=self.user,
#                 embeddings=[0.01] * 1536 
#             )

#     def create_hnsw_index(self):
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 CREATE INDEX product_embeddings_hnsw_idx
#                 ON post_product USING hnsw (embeddings vector_cosine_ops);
#             """)

#     def test_search_performance_1000(self):
#         self.create_products(1000)
#         self._test_search_performance()

#     def _test_search_performance(self):
#         data = {
#             'query': 'test query'
#         }
        
#         times = []
#         for _ in range(5):  # 5번 반복하여 평균 시간 계산
#             start_time = time.time()
#             response = self.client.post(self.url, data, format='json')
#             end_time = time.time()
#             times.append(end_time - start_time)
        
#         avg_time = sum(times) / len(times)
        
#         self.assertEqual(response.status_code, 200)
#         print(f"HNSW TEST - Average search execution time with {Product.objects.count()} products: {avg_time} seconds")