from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Recommendation(models.Model):
    author = models.OneToOneField(User, related_name='recommend', blank=True, null=True,
                                  on_delete=models.CASCADE, unique=True)
    members = models.ManyToManyField('account.CustomUser', related_name='recommend_members')
    posts = models.ManyToManyField('post.Post', related_name='recommend_posts')

    def __str__(self):
        return f'{self.author} REC MODEL'

    class Meta:
        ordering = ('author',)
