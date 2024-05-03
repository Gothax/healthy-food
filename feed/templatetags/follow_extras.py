from django import template
from follow.models import Follow

register = template.Library()

@register.filter(name='is_following')
def is_following(user, other_user):
    return Follow.objects.filter(follower=user, following=other_user).exists()
