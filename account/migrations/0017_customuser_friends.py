# Generated by Django 4.1.7 on 2023-03-31 21:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_remove_customuser_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='related_friends', to=settings.AUTH_USER_MODEL),
        ),
    ]