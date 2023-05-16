from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm, LoginForm, signupForm
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth import get_user_model, authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import User
# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('posts:index')
    
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:index')

    if request.method == 'POST':
        form = signupForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            if User.objects.filter(username=username).exists():
                return HttpResponse(f'Username {username} is already exist')
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
            )
            return redirect('accounts:login')
    else:
        form = signupForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def delete(request):
    request.user.delete()
    return redirect('posts:index')


@login_required
def edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/edit.html', context)


def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def follow(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)

    if person != request.user:
        if request.user in person.followers.all():
            person.followers.remove(request.user)
            is_followed = False
        else:
            person.followers.add(request.user)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followings_count': person.followings.count(),
            'followers_count': person.followers.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:profile', person.username)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['profile_image']
    template_name = 'accounts/edit.html'

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {'profile_image_url': self.object.profile_image.url}
            return JsonResponse(data)
        else:
            return response

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'username': self.request.user.username})
        