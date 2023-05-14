from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Comment, Notification

@receiver(post_save, sender=Post.like_users)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        sender = instance.user
        receiver = post.user
        if sender != receiver:
            Notification.objects.create(post=post, sender=sender, receiver=receiver, notification_type=Notification.LIKE)
            
@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        sender = instance.user
        receiver = post.user
        if sender != receiver:
            Notification.objects.create(post=post, sender=sender, receiver=receiver, notification_type=Notification.COMMENT)
