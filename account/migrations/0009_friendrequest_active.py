# Generated by Django 4.1.7 on 2023-03-28 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_customuser_private_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
