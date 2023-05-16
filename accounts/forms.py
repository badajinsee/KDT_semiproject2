from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model, authenticate, login as django_login

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_image', 'status_message')


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        self.user = authenticate(
            username=username,
            password=password
        )

        if not self.user:
            raise forms.ValidationError(
                'Invalid login credentials!'
            )
        else:
            # 자기자신에 login() 메서드 추가
            setattr(self, 'login', self._login)

    def _login(self, request):
        django_login(request, self.user)


User = get_user_model()

class signupForm(forms.Form):
    username = forms.CharField(
        label='아이디',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),)
    
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}),)
    
    email = forms.EmailField(
        label='이메일',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),)

    first_name = forms.CharField(
        label='성함',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}),)

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('Username already exists!')
        return data