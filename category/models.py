from django.db import models

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return f'{self.name}'


class SubCategory(models.Model):
    class Meta:
        verbose_name_plural = 'SubCategories'

    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey(Category, related_name='subs', on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.name}--||--{self.parent_category}'
