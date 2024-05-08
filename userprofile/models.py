from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(blank=True, null=True, upload_to = 'user_images/', default='default_profile_image.png')
    nickname = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    detailed_address = models.CharField(max_length=100)
    is_seller = models.BooleanField(default=False)  # 판매자 여부
    
    def __str__(self):
        return self.user.username
