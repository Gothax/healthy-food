import uuid
from django.db import models
from django.utils.timesince import timesince
from django.conf import settings

from account.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField()
    name = models.CharField(max_length=100)
    specific = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CONTENT_TYPES = {
        'post': '게시글',
        'review': '리뷰',
        'product': '상품',
    }
    body = models.TextField(blank=True, null=True)
    
    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='post')
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, related_name='posts')


    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)

class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    post = models.ForeignKey(Post, related_name='attachments', on_delete=models.CASCADE)
    
    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        return ''

   
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) 

    class Meta:
        ordering = ('-created_at',)
    
    def created_at_formatted(self):
       return timesince(self.created_at)

class Trend(models.Model):
    hashtag = models.CharField(max_length=255)
    occurences = models.IntegerField()