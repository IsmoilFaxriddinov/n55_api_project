# Generated by Django 5.1.6 on 2025-02-18 16:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='postclapmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_claps', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postcommentclapmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_comments_claps', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postcommentmodel',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='posts.postcommentmodel'),
        ),
        migrations.AddField(
            model_name='postcommentmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postcommentclapmodel',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.postcommentmodel'),
        ),
        migrations.AddField(
            model_name='postmodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postcommentmodel',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.postmodel'),
        ),
        migrations.AddField(
            model_name='postclapmodel',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claps', to='posts.postmodel'),
        ),
        migrations.AddField(
            model_name='postmodel',
            name='topics',
            field=models.ManyToManyField(related_name='posts', to='posts.topicmodel'),
        ),
    ]
