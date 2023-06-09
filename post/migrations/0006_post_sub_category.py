# Generated by Django 4.1.8 on 2023-04-24 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_subcategory'),
        ('post', '0005_alter_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='category.subcategory'),
        ),
    ]
