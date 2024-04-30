from django.shortcuts import render, get_object_or_404,redirect #redirect추가
from .models import Content, FeedImage
from django.contrib.auth.models import User
from userprofile.models import Profile
from django.views.generic import ListView, CreateView
from .models import *
from .forms import ContentForm, ReviewContentForm, CommentForm
from django.urls import reverse_lazy

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
    commentform = CommentForm()  # (추가) forms.py에있는 CommentForm 가지고옴
    return render(request, 'feed/post_detail.html', {'post': post,'commentform':commentform})  #(추가)
# -----------------댓글저장 로직 추가--------------------------------------------

def comments_create(request, pk):
    if request.method == 'POST':
        content = get_object_or_404(Content, pk=pk)  # 게시물을 번호가지고옴
        commentform = CommentForm(request.POST) # 값을받아 폼에 저장
        if commentform.is_valid():
            comment = commentform.save(commit=False) # commit=False -> 임시저장
            comment.user = request.user  # 현재 사용자를 댓글 작성자로 지정
            comment.content = content  # 게시물 번호 가져와서 게시물 지정함
            comment.save() #DB저장

    return redirect('feed:post_detail', pk=pk) #저장하고 그자리

