from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import json
from account.models import User
from post.models import Post, Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile
import time


class SearchPerformanceTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('search')
        self.user = User.objects.create_user(name='testuser', email='testuser@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.category = Category.objects.create(id=1, name='TestCategory')

    def create_products(self, count):
        for i in range(count):
            Product.objects.create(
                category=self.category,
                price=100,
                name=f'TestProduct{i}',
                specific='TestSpecific',
                seller=self.user,
                embeddings=[0.01] * 1536 
            )

    # def test_search_performance_10(self):
    #     self.create_products(10)
    #     self._test_search_performance()

    # def test_search_performance_100(self):
    #     self.create_products(100)
    #     self._test_search_performance()

    def test_search_performance_1000(self):
        self.create_products(1000)
        self._test_search_performance()

    def _test_search_performance(self):
        data = {
            'query': 'test query'
        }
        
        start_time = time.time()
        response = self.client.post(self.url, data, format='json')
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        print(f"Search execution time with {Product.objects.count()} products: {end_time - start_time} seconds")