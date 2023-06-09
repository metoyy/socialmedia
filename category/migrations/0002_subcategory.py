# Generated by Django 4.1.8 on 2023-04-24 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='subs', to='category.category')),
            ],
            options={
                'verbose_name_plural': 'SubCategories',
            },
        ),
    ]
