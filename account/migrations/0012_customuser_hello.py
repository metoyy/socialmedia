# Generated by Django 4.1.7 on 2023-03-31 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_remove_customuser_favorite_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='hello',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
