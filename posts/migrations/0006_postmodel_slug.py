# Generated by Django 5.1.6 on 2025-02-10 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_remove_postmodel_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
