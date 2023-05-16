from django.shortcuts import render, redirect
from .models import Post, PostImage, Comment, Notification
from accounts.models import User
from .forms import PostForm, PostImageForm, CommentForm
from django.db.models import Q


# Create your views here.
def index(request):
    posts = Post.objects.filter(user__in=request.user.followings.all()).order_by('-updated_at')
    users = User.objects.exclude(Q(followers=request.user) | Q(id=request.user.id))
    context = {
        "posts": posts,
        "users": users,
    }

    return render(request, "posts/index.html", context)


def detail(request, post_pk):
    posts = Post.objects.all()
    post = Post.objects.get(pk=post_pk)

    comment_form = CommentForm()
    comments = post.comment_set.filter(
        parent_comment__isnull=True
    )  # Comment.objects.filter(post=post)
    cocomments = post.comment_set.exclude(parent_comment__isnull=True)

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
        print('\n')
        print("여기는 form",form) 
        print('\n')
        print("여기는 imageForm",imageForm)
        print('\n')
        if form.is_valid() and imageForm.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            form.save()

            for image in request.FILES.getlist("image"):
                PostImage.objects.create(post=post, image=image)
            return redirect("posts:detail", post.pk)

    else:
        form = PostForm()
        imageForm = PostImageForm()

    context = {
        "form": form,
        "imageForm": imageForm,
    }

    return render(request, "posts/create-ex.html", context)


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
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        if parent_pk != 0:
            comment.parent_comment = Comment.objects.get(pk=parent_pk)
        # comment.user = request.user
        comment_form.save()
        return redirect("posts:detail", post.pk)
    context = {
        "post": post,
        "comment_form": comment_form,
    }
    return render(request, "posts/detail.html", context)


def comments_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    # if request.user == comment.user:
    comment.delete()
    return redirect("posts:detail", post_pk)


def notifications(request):
    notifications = Notification.objects.filter(
        user=request.user, is_read=False
    ).order_by("-created_at")
    return render(request, "posts/notifications.html", {"notifications": notifications})
