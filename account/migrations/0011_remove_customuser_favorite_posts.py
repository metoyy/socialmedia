# Generated by Django 4.1.7 on 2023-03-29 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_customuser_favorite_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='favorite_posts',
        ),
    ]
