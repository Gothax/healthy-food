from django.shortcuts import render, get_object_or_404, redirect
from .models import Content, FeedImage, Like
from django.contrib.auth.models import User
from userprofile.models import Profile
from django.views.generic import ListView, CreateView, DetailView
from .models import *
from .forms import ContentForm, ReviewContentForm, CommentForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages

def post_edit(request, pk):
    post = get_object_or_404(Content, pk=pk)
    if request.user != post.user and not request.user.is_staff:
        messages.error(request, "게시글을 수정할 권한이 없습니다.")
        return redirect('feed:index')
    
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=post)
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
        form = ContentForm(instance=post)
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
    paginate_by = 8

# 일반 게시물 작성에 라우팅
class ContentCreateView(CreateView):
    model = Content
    form_class = ContentForm
    template_name = 'feed/post_create.html'
    success_url = reverse_lazy('feed:post-create')  # 생성 성공 후 리다이렉트
    
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
        # 폼 데이터 저장 전 미리 인스턴스를 만들지만, DB에는 아직 저장하지 않음
        self.object = form.save(commit=False)
        self.object.user = self.request.user  
        self.object.content_type = 'post'  
        self.object.save()  # DB에 저장

        # 이미지 처리
        images = self.request.FILES.getlist('images')  # 'images'는 템플릿에서 input 태그의 name 속성값
        for image in images:
            FeedImage.objects.create(content=self.object, image=image)  # 각 이미지에 대해 FeedImage 인스턴스 생성 및 저장
        
        return super().form_valid(form)
    

    
# 구매기록에서 라우팅
class ReviewCreateView(CreateView):
    model = Content
    form_class = ReviewContentForm
    template_name = 'feed/review_create.html' 
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.content_type = 'review'
        return super().form_valid(form)

def post_detail(request, pk):
    post = get_object_or_404(Content, pk=pk)
    commentform = CommentForm()  
    return render(request, 'feed/post_detail.html', {'post': post,'commentform':commentform})  

def comments_create(request, pk):
    if request.method == 'POST':
        content = get_object_or_404(Content, pk=pk)  
        commentform = CommentForm(request.POST) 
        if commentform.is_valid():
            comment = commentform.save(commit=False) 
            comment.user = request.user  # 현재 사용자를 댓글 작성자로 지정
            comment.content = content  # 게시물 번호 가져와서 게시물 지정함
            comment.save() #DB저장

    return redirect('feed:post_detail', pk=pk) 

# 댓글삭제 
def comments_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()

    return redirect('feed:post_detail', pk=comment.content.pk)
        
def view_user(request, pk):
    user = User.objects.get(pk=pk)
    posts = Content.objects.filter(user=pk, content_type='post')
    reviews = Content.objects.filter(user=pk, content_type='review')
    context = {'user': user,
                'posts': posts,
                'reviews': reviews,
                }
    return render(request, 'feed/view_user_page.html', context)