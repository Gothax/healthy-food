from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Follow
from django.contrib.auth.models import User
from django.views import generic
from product.models import Product
from feed.models import Content
from userprofile.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from config.forms import ProfileForm

def index(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'follow/index.html', {'users': users})

class UserLV(generic.ListView):
    model = User
    template_name = 'follow/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 사용자가 판매자 그룹에 속해있는지 확인
        context['is_seller'] = self.request.user.groups.filter(name='Sellers').exists()
        context['posts'] = Content.objects.filter(user=self.request.user)
        context['userprofile'] = self.request.user.profile
        return context


# 팔로우/언팔로우 처리
@login_required
def follow_unfollow(request, user_id):
    other_user = get_object_or_404(get_user_model(), pk=user_id)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=other_user)
    # 이미 팔로우되어 있다면, 기록을 삭제(언팔로우)
    if not created:
        follow.delete()
    return redirect('feed:view_user', pk=user_id)

class SellerProductLV(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Product
    template_name = 'follow/seller_page.html'
    context_object_name = 'products'
    login_url = reverse_lazy('follow:index')

    def test_func(self): # 현재 유저가 그룹에 속하면 접속, 아니면 403 에러
        # 현재 로그인한 사용자가 Sellers 그룹에 속해 있는지 확인
        return self.request.user.groups.filter(name='Sellers').exists()
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_images = {}
        for product in context['products']:
            product_images[product.id] = product.images.first().image_url if product.images.exists() else None
        context['product_images'] = product_images
        context['received_reviews'] = Content.objects.filter(seller=self.request.user.id, content_type='review')

        return context
    
# def edit_profile(request):
#     try:
#         profile = request.user.profile
#     except User.profile.RelatedObjectDoesNotExist:
#         profile = None

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             # form.save() 호출 시 user 인자를 전달
#             new_profile = form.save(user=request.user)
#             # 성공적으로 프로필이 저장되었다면 원하는 페이지로 리다이렉트
#             return redirect('follow:user_detail')
#     else:
#         form = ProfileForm(instance=profile)

#     return render(request, 'follow/edit_profile.html', {'form': form})

def edit_profile(request):
    try:
        profile = request.user.profile
    except User.profile.RelatedObjectDoesNotExist:
        profile = None

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            # 사용자 모델 저장
            new_profile = profile_form.save(user=request.user, commit=False) # User 모델과 Profile 모델 연결
            new_profile.save()  # 프로필 모델 DB에 저장
            return redirect('follow:user_detail')  # 가입 완료 페이지로 리다이렉트
    else:
        profile_form = ProfileForm(instance=profile)

    context = {
        'profile_form': profile_form,
    }
    return render(request, 'follow/edit_profile.html', context)