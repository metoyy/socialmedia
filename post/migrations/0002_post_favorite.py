# Generated by Django 4.1.7 on 2023-03-29 10:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorite_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]