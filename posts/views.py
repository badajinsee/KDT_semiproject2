from django.shortcuts import render, redirect
from .models import Post, PostImage, Comment, Notification
from accounts.models import User
from .forms import PostForm, PostImageForm, CommentForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
@login_required
def index(request):
    following_posts = Post.objects.filter(user__in=request.user.followings.all()).order_by('-created_at')
    other_posts = Post.objects.exclude(user__in=request.user.followings.all()).order_by('-created_at')
    # print('\n' + following_posts + '\n' + other_posts + '\n')
    posts = list(following_posts) + list(other_posts)
    # print('\n' + posts + '\n')
    
    context = {
        "posts": posts,
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
    post = Post.objects.get(pk=post_pk)
    content = request.POST.get('content')
    if content:
        comment = Comment(
            post=post,
            user=request.user,
            content=content
        )
        
        if parent_pk != 0:
            comment.parent_comment = Comment.objects.get(pk=parent_pk)
        
        # 추가적인 유효성 검사 로직을 수행할 수 있습니다.
        
        comment.save()
        
        # 댓글 저장 후의 처리 로직을 추가할 수 있습니다.
        print("도달데스까")
        context = {
            "content": content,
            "postPk": post.pk,
            "commentPk": comment.pk,
            "postUser": post.user.username,
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


def notification_list(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    context = {
        'notifications': notifications
    }
    return render(request, 'posts/notification.html', context)

def notification_mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('notifications:notification_list')
