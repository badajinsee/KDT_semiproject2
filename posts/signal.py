from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from django.urls import reverse
from notifications.signals import notify

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, **kwargs):
    post = instance.post
    comment_user = instance.user
    post_user = post.user
    if comment_user != post_user:
            # 알림 생성
            recipient = post_user
            verb = f"{comment_user.username}님이 답글을 남겼습니다."
            action_object = instance
            url = reverse('detail', kwargs={'pk': post.pk})
            notify.send(comment_user, recipient=recipient, verb=verb, action_object=action_object, url=url)
