# Generated by Django 4.1.8 on 2023-04-24 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_subcategory'),
        ('post', '0004_post_members_post_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='category.category'),
        ),
    ]
