from django.utils import timezone
from django import template

register = template.Library()

@register.filter
def custom_timesince(value):
    now = timezone.now()
    diff = now - value
    
    if diff.days >= 365:
        years = diff.days // 365
        return f'{years}년 전'
    elif diff.days >= 30:
        months = diff.days // 30
        return f'{months}달 전'
    elif diff.days > 0:
        return f'{diff.days}일 전'
    elif diff.seconds // 3600 > 0:
        return f'{diff.seconds // 3600}시간 전'
    elif diff.seconds // 60 > 0:
        return f'{diff.seconds // 60}분 전'
    else:
        return '방금 전'
