from django.contrib import admin

from activity.models import Activity


# Register your models here.


@admin.register(Activity)
class Act(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category')
