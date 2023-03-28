from django.contrib.auth import get_user_model
from django.db import models

from post.models import Post


User = get_user_model()


class Like(models.Model):
    owner = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['owner', 'post']

