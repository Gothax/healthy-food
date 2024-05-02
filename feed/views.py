from django.shortcuts import render, get_object_or_404, redirect
from .models import Content, FeedImage, Like
from django.contrib.auth.models import User
from userprofile.models import Profile
from django.views.generic import ListView, CreateView
from .models import *
from .forms import ContentForm, ReviewContentForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from django.http import JsonResponse


@login_required
def like_content(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    like_qs = Like.objects.filter(user=request.user, content=content)

    if like_qs.exists():
        like_qs[0].delete()  # 이미 '좋아요'를 눌렀다면 삭제하여 '좋아요' 취소
    else:
        Like.objects.create(user=request.user, content=content)  # '좋아요' 추가

    return redirect(reverse('feed:post_detail', args=(content.id, )))

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

    # 댓글을 좋아요 개수를 기준으로 정렬하여 가져옴
    comments = post.comment_set.annotate(num_likes=Count('likes')).order_by('-num_likes')

    # 가장 많은 좋아요를 받은 첫 번째 댓글을 설정
    most_liked_comment = comments.first()

    # most_liked_comment이 None이 아닌 경우에만 나머지 댓글을 날짜순으로 정렬하여 가져옴
    other_comments = None
    if most_liked_comment:
        other_comments = comments.exclude(pk=most_liked_comment.pk).order_by('-created_at')

    # 댓글의 총 개수 계산
    comments_count = comments.count()

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
    posts = Content.objects.filter(user=pk, content_type='post')
    reviews = Content.objects.filter(user=pk, content_type='review')
    context = {'user': user,
                'posts': posts,
                'reviews': reviews,
                }
    return render(request, 'feed/view_user_page.html', context)
        
# 댓글수정
from django.core.exceptions import PermissionDenied

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

