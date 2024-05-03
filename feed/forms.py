from django import forms
from .models import Content, Comment

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'body_text',]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    

class CommentForm(forms.ModelForm):
    class Meta: 
        model = Comment 
        fields = ['comment_text'] 
        exclude = ('user',)  # user 필드를 제외


	   
