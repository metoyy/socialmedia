from django.contrib import admin

from category.models import Category, SubCategory


# Register your models here.


@admin.register(Category)
class Cat(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SubCategory)
class Sub(admin.ModelAdmin):
    list_display = ('name', 'parent_category')
    search_fields = ('name',)
    list_filter = ('parent_category',)
