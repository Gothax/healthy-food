from django import forms
from .models import Content, FeedImage,Comment
from django.forms import inlineformset_factory

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'body_text']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data



class ReviewContentForm(ContentForm):
    class Meta(ContentForm.Meta):
        fields = ContentForm.Meta.fields + ['product', 'seller']

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        seller = cleaned_data.get("seller")

        if not product or not seller:
            raise forms.ValidationError("구매한 상품만 리뷰할 수 있습니다.")
        return cleaned_data
    

class CommentForm(forms.ModelForm):
    class Meta: # (내부 클래스 메타에 모델 어떤거 쓸건지)
        model = Comment 
        fields = ['comment_text'] # (입력 받고자 하는 fields)
        exclude = ('user',)  # 'user' 필드를 제외합니다.

	   
