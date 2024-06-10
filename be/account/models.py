from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.conf import settings


class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, default='', unique=True) #nickname
    user_image = models.ImageField(upload_to='user_image', blank=True, null=True, default='default_profile_image.png')

    # 가입 후 주문할때 받는 영역
    real_name = models.CharField(max_length=15, blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    detailed_address = models.CharField(max_length=100)
    is_seller = models.BooleanField(default=False)  # 판매자 여부
    business_number = models.CharField(max_length=100, blank=True)

    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def get_userimage(self):
        return settings.WEBSITE_URL + self.user_image.url
