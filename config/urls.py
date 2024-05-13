"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from product import views as product_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # 로그인, 회원가입
    path('login/', views.login, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register_user, name='register'),
    path('accounts/register/done/', views.UserCreateDoneTV.as_view(), name='register_done'),
    path('check_duplicate/', views.check_duplicate, name='check_duplicate'),
    path('user_profile_image/', views.user_profile_image, name='user_profile_image'),

    # 팔로우, 팔로잉
    path('user/', include('follow.urls')),
    # 상품
    path('product/', include('product.urls')),
    path("cart/", include("cart.urls")),
    # 게시글(댓글, 좋아요)
    path("feed/", include("feed.urls")),
    # 주문 생성
    path("orders/", include("orders.urls")),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
