# Generated by Django 5.1.6 on 2025-02-19 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_confirmationmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationmodel',
            name='expire_minutes',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
