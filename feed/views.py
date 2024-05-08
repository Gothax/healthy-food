from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.views import View
from .models import *
from userprofile.models import Profile
from orders.models import OrderItem
from .forms import ContentForm, CommentForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.utils.html import escape
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.template.loader import render_to_string

def post_edit(request, pk):
    post = get_object_or_404(Content, pk=pk)
    # 요청한 사용자가 게시글을 작성한 사용자가 아니고, 스태프도 아닐 경우
    if request.user != post.user and not request.user.is_staff:
        # 'feed:index'로 리다이렉트
        return redirect('feed:index')

    # POST 요청을 처리하는 경우
    if request.method == 'POST':
        # 제출된 데이터와 파일을 포함한 폼을 생성
        form = ContentForm(request.POST, request.FILES, instance=post)
        # 폼이 유효할 경우
        if form.is_valid():
            saved_post = form.save()  # 폼 데이터 저장

            # 이미지 처리 로직 추가
            images = request.FILES.getlist('images')  # images는 템플릿에서 이미지 파일 <input> 태그의 name 속성값입니다.
            if images:
                FeedImage.objects.filter(content=saved_post).delete()  # 기존 이미지 삭제
                for image in images:
                    FeedImage.objects.create(content=saved_post, image=image)  # 새 이미지 저장

            messages.success(request, "게시글이 성공적으로 수정되었습니다.")
            return redirect('feed:post_detail', pk=saved_post.pk)
    else:
        # 게시글 인스턴스를 포함한 폼을 생성
        form = ContentForm(instance=post)
    # 'feed/post_edit.html' 템플릿을 렌더링하고, 폼과 게시글 객체를 컨텍스트로 전달
    return render(request, 'feed/post_edit.html', {'form': form, 'post': post})


def post_delete(request, pk):
    post = Content.objects.get(pk=pk)
    if request.user == post.user or request.user.is_staff:  # 접근 권한 확인
        post.delete()
        messages.success(request, "게시글이 성공적으로 삭제되었습니다.")
        return redirect('feed:index')
    else:
        messages.error(request, "게시글을 삭제할 권한이 없습니다.")
        return redirect('feed:index')



def like_content(request, content_id):
    if request.method == 'POST':
        content = Content.objects.get(id=content_id)
        user = request.user
        if user in content.likes.all():
            content.likes.remove(user)
            is_liked = False
        else:
            content.likes.add(user)
            is_liked = True
        context = {
            'likes_count': content.likes.count(),
            'is_liked': is_liked,
        }
        return JsonResponse(context)
    else:
        # 비정상적인 접근을 405 Method Not Allowed로 처리
        return JsonResponse({'error': 'Invalid request'}, status=405)


class ContentListView(ListView):
    model = Content
    template_name = "feed/post_all.html"
    context_object_name = 'posts'
    paginate_by = 16

    def get_queryset(self):
        # 'created_at' 필드를 기준으로 역순으로 정렬합니다. 실제 필드명에 맞게 변경해 주세요.
        return Content.objects.all().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.object_list = self.get_queryset()
            page = request.GET.get('page', 1)
            paginator = self.get_paginator(self.object_list, self.paginate_by)

            try:
                posts = paginator.page(int(page))
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = []

            post_data = []
            for post in posts:
                post_data.append(render_to_string('feed/post_card.html', {'post': post}, request=request))

            return JsonResponse({'posts': post_data}, safe=False)

        return super().get(request, *args, **kwargs)
    
@require_GET
def user_search(request):
    query = request.GET.get('q', '')
    if query:
        # users = User.objects.filter(username__icontains=query)
        # user_list = list(users.values('username'))
       
        users = Profile.objects.filter(nickname__icontains=query)
        user_list = list(users.values('nickname'))
        return JsonResponse(user_list, safe=False)
    return JsonResponse([], safe=False)

# 일반 게시물 작성에 라우팅
class ContentCreateView(View):
    template_name = 'feed/post_create.html'
    success_url = reverse_lazy('feed:post-create')
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        body_text = request.POST.get('body_text')
        images = request.FILES.getlist('images')  # 여러 이미지 파일을 리스트로 받음
        
        if not title or not body_text:
            # 필수 필드가 비어있는 경우 에러 처리
            return HttpResponseBadRequest("제목과 본문은 필수 항목입니다.")
        
        # Content 인스턴스 생성
        content = Content.objects.create(
            user=request.user,
            title=title,
            body_text=body_text,
            content_type='post'
        )
        
        # 이미지 처리
        for image in images:
            FeedImage.objects.create(content=content, image=image)
        
        # 성공 시 리디렉션
        return redirect(self.success_url)
    
def add_product_info_to_session(request):
    product_id = request.GET.get('product_id')
    seller_id = request.GET.get('seller_id')
    order_id = request.GET.get('order_id')
    # 세션에 product_id와 seller_id 저장
    request.session['product_id'] = product_id
    request.session['seller_id'] = seller_id
    request.session['order_id'] = order_id
    return redirect('feed:review-create')

    
# 구매기록에서 라우팅
class ReviewCreateView(CreateView):
    model = Content
    form_class = ContentForm
    template_name = 'feed/post_create.html'
    success_url = reverse_lazy('orders:order_history')  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        seller_id = self.request.session.get('seller_id')
        product_id = self.request.session.get('product_id')
        
        # 정상적인 경로로 리뷰를 작성하는 지 확인하는 로직
        if not seller_id or not product_id:
            return HttpResponseForbidden('구매기록에서 리뷰를 작성해 주세요.')

        seller = get_object_or_404(User, id=seller_id)
        product = get_object_or_404(Product, id=product_id, seller=seller)
        
        
        # 현재 request를 보낸 user의 구매 기록을 조회
        # 구매한 상품에 대해 리뷰를 작성하는 것인지 확인하는 로직
        user_has_purchased = OrderItem.objects.filter(
                            order__user=self.request.user, 
                            product=product
                         ).exists()

        if not user_has_purchased:
            return HttpResponseForbidden('구매한 상품만 리뷰할 수 있습니다.')
        


        
        # 폼 데이터 저장 전 미리 인스턴스를 만들지만, DB에는 아직 저장하지 않음
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.seller_id = seller_id
        self.object.product_id = product_id
        self.object.content_type = 'review'
        self.object.save()
        
        # 주문 id와 product로 조회한 주문 구성요소
        order_item = OrderItem.objects.get(
        order__id=self.request.session.get('order_id'),  
        product_id=product_id,
    )
        
        if order_item:
            order_item.review = self.object  
            order_item.save()  

        # 이미지 처리
        images = self.request.FILES.getlist('images')  # 'images'는 템플릿에서 input 태그의 name 속성값
        for image in images:
            FeedImage.objects.create(content=self.object, image=image)  # 각 이미지에 대해 FeedImage 인스턴스 생성 및 저장
        
        # 세션에서 삭제
        del self.request.session['seller_id']
        del self.request.session['product_id']
        del self.request.session['order_id']
        return super().form_valid(form)
    
# 본문 전체를 탐색하고 @user 를 link로 반환 -> 최적화 필요
# detail view에서 본문을 출력하는 부분에 사용
def convert_usernames_to_links(text):
    words = escape(text).split()
    for i, word in enumerate(words):
        if word.startswith('@'):
            username = word[1:]
            profile = Profile.objects.filter(nickname=username).first()
            if profile:
                user_url = reverse('feed:view_user', kwargs={'pk': profile.user.pk})
                words[i] = f'<a href="{user_url}">@{username}</a>'
    return ' '.join(words)

def post_detail(request, pk):
    post = get_object_or_404(Content, pk=pk)
    commentform = CommentForm()  
    
    # 본문에 태그된 user에 링크를 걸어줌
    post.body_text = convert_usernames_to_links(post.body_text)

    # 댓글을 좋아요 개수를 기준으로 정렬하여 가져옴
    comments = post.comment_set.annotate(num_likes=Count('likes')).order_by('-num_likes')

    # 가장 많은 좋아요를 받은 첫 번째 댓글을 설정
    most_liked_comment = comments.first()

    # most_liked_comment이 None이 아닌 경우에만 나머지 댓글을 날짜순으로 정렬하여 가져옴
    other_comments = None
    if most_liked_comment:
        other_comments = comments.exclude(pk=most_liked_comment.pk).order_by('-created_at')

    # 댓글의 총 개수 계산
    comments_count = comments.count() #추가

    return render(request, 'feed/post_detail.html', {'post': post, 'commentform': commentform, 'most_liked_comment': most_liked_comment, 'other_comments': other_comments, 'comments_count': comments_count})


@login_required
def comments_create(request, pk):
    if request.method == 'POST':
        content = get_object_or_404(Content, pk=pk)  
        commentform = CommentForm(request.POST) 
        if commentform.is_valid():
            comment = commentform.save(commit=False) 
            comment.user = request.user  
            comment.content = content  
            comment.save() 
            return redirect('feed:post_detail', pk=pk) 
            
    else:
        return redirect(reverse('login')) # 로그인안하면 로그인창으로

# 댓글삭제 
def comments_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()

    return redirect('feed:post_detail', pk=comment.content.pk)


def view_user(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_active == True:
        if request.user.id != pk:
            products = Product.objects.filter(seller=pk).prefetch_related('images')
            product_images = {}
            for product in products:
                product_images[product.id] = product.images.first().image_url if product.images.exists() else None
            received_reviews = Content.objects.filter(seller=pk, content_type='review')
            posts = Content.objects.filter(user=pk)
            is_seller = User.objects.get(pk=pk).groups.filter(name='Sellers').exists()
            userprofile = user.profile
            context = {'user': user,
                        'posts': posts,
                        'is_seller': is_seller,
                        'products': products,
                        'product_images': product_images,
                        'received_reviews': received_reviews,
                        'userprofile': userprofile,
                        }
            return render(request, 'feed/view_user_page.html', context)
        else:
            return redirect('follow:user_detail')
    else:
        return HttpResponseForbidden("비활성화된 유저입니다.")


def comments_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # 현재 요청을 보낸 사용자와 댓글의 작성자를 비교하여 권한을 검사
    if request.user != comment.user:
        # 권한이 없는 경우 404 에러 대신에 PermissionDenied 예외 발생
        raise PermissionDenied("댓글 수정 권한이 없습니다.")
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('feed:post_detail', pk=comment.content.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'feed/comment_update.html', {'form': form})


# 댓글좋아요
@login_required
def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        # 현재 로그인한 사용자가 해당 댓글을 이미 좋아요 했는지 확인
        if request.user in comment.likes.all():
            # 이미 좋아요한 경우, 좋아요 취소
            comment.likes.remove(request.user)
            liked = False
        else:
            # 좋아요 추가
            comment.likes.add(request.user)
            liked = True
        # 좋아요 수를 반환
        likes_count = comment.likes.count()
        return JsonResponse({'liked': liked, 'likes_count': likes_count})
    else:
        return JsonResponse({}, status=405)  # POST 요청만 허용