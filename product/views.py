from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from cart.forms import AddProductForm

"""login_required -> 판매자 인증기능 필요, 개발 후 수정(판매자일 경우에 접근 가능)
판매자 관점의 함수

Returns:
    _type_: _description_
"""
@login_required
def seller_index(request):
    product = Product.objects.all().filter(user__id = request.user.id)
    context = {
        'object_list' : product
    }
    return render(request, 'product/seller_index.html', context)

@login_required
def add_product(request):
    if request.method == "POST":
        user = request.user
        product_name = request.POST.get('productname')
        product_price = request.POST['price']
        description = request.POST.get('description')
        specific = request.POST.get('specific')
        category_id = request.POST.get('category')  # 카테고리 ID 추가
        
        # 카테고리 객체 가져오기
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            # 적절한 에러 처리 또는 기본 카테고리 설정
            return render(request, 'error_page.html', {'error': 'Category does not exist'})

        product = Product.objects.create(
            seller=user,
            name=product_name,
            price=product_price,
            description=description,
            specific=specific,
            category=category,  # 카테고리 설정
        )
        
        # 파일이 여러 개일 경우 request.FILES.getlist를 사용
        if 'files' in request.FILES:
            fs = FileSystemStorage()
            for uploaded_file in request.FILES.getlist('files'):
                name = fs.save(uploaded_file.name, uploaded_file)
                url = fs.url(name)
                ProductImage.objects.create(product=product, image_url=url)

        return redirect('product:add_product')  # 데이터 저장 후 페이지 재로드

    # GET 요청 처리
    categories = Category.objects.all()  # 카테고리 목록을 템플릿에 전달
    return render(request, 'product/add_product.html', {'categories': categories})


def product_delete(request, pk):
    object = Product.objects.get(pk=pk)
    object.delete()
    return redirect('product:seller_index')      

"""ProductListView
구매자 관점의 product list

Returns:
    category id가 주어지지 않으면 전체 상품 return
    주어지면 해당 상품만 return
"""
class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            return Product.objects.filter(category=category, seller__is_active=True).prefetch_related('images')
        return Product.objects.filter(seller__is_active=True).prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category_id'] = int(self.kwargs.get('category_id', '0'))

        # 각 제품에 대한 기본 이미지 URL을 추가
        product_images = {}
        for product in context['products']:
            product_images[product.id] = product.images.first().image_url if product.images.exists() else None
        context['product_images'] = product_images

        return context
    
def product_detail(request, pk):
    object = Product.objects.get(pk=pk)
    add_to_cart = AddProductForm(initial={'quantity': 1})
    
    context = {
        'object':object,
        'add_to_cart': add_to_cart,
    }
    return render(request, 'product/product_detail.html', context,)

