# Generated by Django 5.1.6 on 2025-02-12 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_alter_postmodel_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('title', models.CharField(max_length=125)),
            ],
            options={
                'verbose_name': 'topic',
                'verbose_name_plural': 'topics',
            },
        ),
        migrations.AddField(
            model_name='postmodel',
            name='topics',
            field=models.ManyToManyField(related_name='posts', to='posts.topicmodel'),
        ),
    ]
