# Generated by Django 4.1.7 on 2023-03-27 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_customuser_private_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='private_account',
            field=models.BooleanField(default=False),
        ),
    ]
