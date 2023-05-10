from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(
            attrs={'class': 'form-control','placeholder': '아이디를 입력하세요',}),)
    

    email = forms.EmailField(
        label='이메일',
        widget=forms.TextInput(
            attrs={'class': 'form-control','placeholder': '이메일을 입력하세요',}),)
    
    
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control','placeholder': '비밀번호를 입력하세요',}),)
    

    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control','placeholder': '비밀번호를 다시 입력하세요',}),)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username','email','password1','password2',)


class CustomUserChangeForm(UserChangeForm):
    profile_image = forms.ImageField(
        label='프로필 이미지',
        widget=forms.FileInput(
            attrs={'id': 'profile-image','class': 'form-control',}),)
    

    status_message = forms.CharField(
        label='상태 메세지',
        widget=forms.TextInput(
            attrs={'id': 'status_message','class': 'form-control',}),)
    

    password = None

    class Meta:
        model = get_user_model()
        fields = ('profile_image','status_message',)