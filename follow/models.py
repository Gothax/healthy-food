from django.db import models
from django.contrib.auth.models import User
from django.db.models.constraints import UniqueConstraint

#review
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['follower', 'following'], name='unique_followers')
        ]

    def __str__(self):
        return f"{self.follower} follows {self.following}"

