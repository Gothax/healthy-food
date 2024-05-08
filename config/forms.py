from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from userprofile.models import Profile
from django.db import transaction
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      # username 필드에 form-control 클래스를 추가
      self.fields['username'].widget.attrs.update({'class': 'form-control'})
      # password1 필드에 form-control 클래스를 추가
      self.fields['password1'].widget.attrs.update({'class': 'form-control', 'type': 'password'})
      # password2 필드에 form-control 클래스를 추가
      self.fields['password2'].widget.attrs.update({'class': 'form-control', 'type': 'password'})

class ProfileForm(forms.ModelForm):
    user_image = forms.ImageField(label='프로필 이미지', required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    nickname = forms.CharField(label='닉네임', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='전화번호', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='주소', widget=forms.TextInput(attrs={'class': 'form-control'}))
    detailed_address = forms.CharField(label='상세 주소', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}))
    is_seller = forms.BooleanField(label='판매자 여부', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Profile
        fields = ('nickname', 'user_image', 'phone_number', 'address', 'detailed_address', 'is_seller')
      
    def clean_nickname(self):
      nickname = self.cleaned_data['nickname']
      # 닉네임에 공백이 있는지 확인
      if ' ' in nickname:
          raise ValidationError("닉네임에는 공백을 포함할 수 없습니다.")
      return nickname

    def save(self, user=None, commit=True):  # user 인자 추가
      profile = super().save(commit=False)  # commit=False로 호출
      if user is not None:
          profile.user = user  # User 인스턴스 연결

      if self.cleaned_data['is_seller']:
          try:
              with transaction.atomic():
                  group = Group.objects.get(name='Sellers')
                  group.user_set.add(user)  # 여기에서는 self.instance.user 대신 user 사용
          except Group.DoesNotExist:
              pass
      return profile