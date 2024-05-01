from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class Content(models.Model):
    CONTENT_TYPES = (
        ('post', '게시글'),
        ('review', '리뷰'),
    )
    user = models.ForeignKey(User, related_name='contents', on_delete=models.CASCADE)
    body_text = models.TextField(blank=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_contents')
    
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='post')
    # !content_type -> review일 경우 product, seller field 설정 필수!
    # review가 아닌 경우 NULL
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_reviews')
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'content')  # 한 사용자가 같은 컨텐츠에 여러 번 '좋아요'를 누르는 것을 방지


class FeedImage(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='feed_images')
    image = models.ImageField(upload_to='feed_images/') 

class Comment(models.Model):
    content = models.ForeignKey(Content,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)  # 댓글을 작성한 사용자
    comment_text = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성일자
    updated_at = models.DateTimeField(auto_now=True) #수정날짜 추가**
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True) # 다 대 다 구조 댓글 좋아요 추가**
