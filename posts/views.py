from django.shortcuts import render, redirect
from .models import Post, PostImage
from .forms import PostForm, PostImageForm

# Create your views here.
def index(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
    }

    return render(request, 'posts/index.html', context)


def detail(request, post_pk):
    posts = Post.objects.all()
    post = Post.objects.get(pk=post_pk)

    context = {
        'posts': posts,
        'post': post,
    }

    return render(request, 'posts/detail.html', context)


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        imageForm = PostImageForm(request.POST, request.FILES)
        if form.is_valid() and imageForm.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            post = form.save()

            for image in request.FILES.getlist('image'):
                PostImage.objects.create(post=post, image=image)
            return redirect('posts:detail', post.pk)

    else:
        form = PostForm()
        imageForm = PostImageForm()

    context = {
        'form': form,
        'imageForm': imageForm,
    }

    return render(request, 'posts/create.html', context)


def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('posts:detail', post.pk)
        else:
            form = PostForm(instance=post)
    else:
        return redirect('posts:index')
    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'posts/update.html', context)
    

def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        post.delete()
    
    return redirect('posts:index')