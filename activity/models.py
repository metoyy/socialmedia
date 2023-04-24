from django.db import models

from category.models import SubCategory


# Create your models here.


class Activity(models.Model):
    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(SubCategory, on_delete=models.RESTRICT, related_name='activity')

