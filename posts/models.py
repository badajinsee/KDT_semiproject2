from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from accounts.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_posts"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)


class PostImage(models.Model):
    def default_image():
        return "default_image_path.jpg"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_images")
    image = ProcessedImageField(
        upload_to="posts/images",
        processors=[ResizeToFill(600, 600)],
        format="JPEG",
        options={"quality": 90},
        blank = False,
        default=default_image,
    )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


