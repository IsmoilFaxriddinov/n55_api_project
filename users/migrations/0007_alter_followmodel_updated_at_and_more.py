# Generated by Django 5.1.6 on 2025-03-05 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_followmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='verificationmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
