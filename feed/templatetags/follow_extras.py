from django import template
from follow.models import Follow

register = template.Library()

@register.filter(name='is_following')
def is_following(user, other_user):
    if not user.is_authenticated:
        # 로그인하지 않은 사용자의 경우 바로 False 반환
        return False
    return Follow.objects.filter(follower=user, following=other_user).exists()
