from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    body = models.TextField(blank=True,)
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    preview = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorite = models.ManyToManyField(User, related_name='favorite_posts', blank=True)

    def __str__(self):
        return f'{self.owner} - {self.title[:50]}'

    class Meta:
        ordering = ('id',)


class PostImages(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)

    def generate_name(self):
        from random import randint
        return 'image' + str(self.id) + '_' + str(randint(100000, 999999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(PostImages, self).save(*args, **kwargs)

# category