from django.shortcuts import render, redirect
from .models import Post, PostImage, Comment
from accounts.models import User
from .forms import PostForm, PostImageForm, CommentForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models.functions import Random
from django.contrib.auth import get_user_model

# Create your views here.
@login_required
def index(request):
    following_posts = Post.objects.filter(Q(user__in=request.user.followings.all()) | Q(user=request.user)).order_by('-created_at')
    other_posts = Post.objects.exclude(Q(user__in=request.user.followings.all()) | Q(user=request.user)).order_by('-created_at')

    # print('\n' + following_posts + '\n' + other_posts + '\n')
    posts = list(following_posts) + list(other_posts)
    # print('\n' + posts + '\n')
    users = User.objects.order_by(Random())[:5]
    if request.is_ajax():
        if request.user in users:
            user = request.user
            user_followed = user.followers.filter(id__in=users.values('id')).exists()
            if user_followed:
                user.followers.remove(user)
                is_followed = False
            else:
                user.followers.add(user)
                is_followed = True
            context = {
                'is_followed': is_followed,
            }
            return JsonResponse(context)
    context = {
        "posts": posts,
        "users": users,
    }

    return render(request, "posts/index.html", context)


def detail(request, post_pk):
    posts = Post.objects.all()
    post = Post.objects.get(pk=post_pk)

    comment_form = CommentForm()
    comments = post.comments.filter(
        parent_comment__isnull=True
    )  # Comment.objects.filter(post=post)
    cocomments = post.comments.exclude(parent_comment__isnull=True)

    context = {
        "posts": posts,
        "post": post,
        "comment_form": comment_form,
        "comments": comments,
        "cocomments": cocomments,
    }

    return render(request, "posts/detail.html", context)


def create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        imageForm = PostImageForm(request.POST, request.FILES)
        if form.is_valid() and imageForm.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            form.save()

            for image in request.FILES.getlist("image"):
                PostImage.objects.create(post=post, image=image)
            return redirect("accounts:profile", post.user.username)

    else:
        form = PostForm()
        imageForm = PostImageForm()

    context = {
        "form": form,
        "imageForm": imageForm,
    }

    return render(request, "posts/create.html", context)


def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            imageForm = PostImageForm(
                request.POST, request.FILES, instance=post.post_images.first()
            )
            if form.is_valid() and imageForm.is_valid():
                form.save()

                # PostImage.objects.filter(post=post).delete()
                for image in request.FILES.getlist("image"):
                    PostImage.objects.create(post=post, image=image)
                return redirect("posts:detail", post.pk)
        else:
            form = PostForm(instance=post)
            imageForm = PostImageForm(instance=post.post_images.first())
    else:
        return redirect("posts:index")
    context = {
        "post": post,
        "form": form,
        "imageForm": imageForm,
    }

    return render(request, "posts/update.html", context)


def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user == post.user:
        post.delete()

    return redirect("posts:index")


def comments_create(request, post_pk, parent_pk):
    print("도달데스까??")
    post = Post.objects.get(pk=post_pk)
    content = request.POST.get('content')
    if content:
        comment = Comment(
            post=post,
            user= request.user,
            content=content
        )
        
        if parent_pk != 0:
            comment.parent_comment = Comment.objects.get(pk=parent_pk)
        
        # 추가적인 유효성 검사 로직을 수행할 수 있습니다.
        
        comment.save()
        print("도달데스까")
        context = {
            "content": content,
            "postPk": post.pk,
            "commentPk": comment.pk,
            "User": request.user.username
        }
        print("도달데스까2")
        return JsonResponse(context)
    
    # content가 없는 경우에 대한 처리 로직을 추가할 수 있습니다.
    
    context = {
        "post": post,
    }
    return render(request, "posts/detail.html", context)


def comments_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    # if request.user == comment.user:
    comment.delete()
    return JsonResponse({})


def search(request):
    keyword = request.GET.get("keyword")

    # if '#' not in keyword:
    #     keyword = '#' + keyword[0:]

    # posts = Post.objects.filter(Q(content__icontains=keyword))    

    users = User.objects.filter(Q(username__icontains=keyword))
    count = users.count()

    context = {
        # "posts": posts, 
        "keyword": keyword, 
        "count": count,
        'users': users,    
    }

    return render(request, 'posts/search.html', context)

@login_required
def like(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
        is_like_users = False
    else:
        post.like_users.add(request.user)
        is_like_users = True
    post.like_count = post.like_users.count()  # 좋아요 개수 업데이트
    post.save()
    context = {
        'is_like_users':is_like_users,
        'like_count': post.like_users.count()  # 좋아요 개수를 추가
    }
    return JsonResponse(context)
    # return redirect('posts:index')


def explore(request):
    posts = Post.objects.all()
    context = {
        "posts": posts,
    }
    return render(request, "posts/explore.html", context)