# Generated by Django 4.1.7 on 2023-03-31 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recomendation', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recommendation',
            options={'ordering': ('members',)},
        ),
        migrations.RemoveField(
            model_name='recommendation',
            name='owner',
        ),
    ]
