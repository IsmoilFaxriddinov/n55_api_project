# Generated by Django 5.1.6 on 2025-02-23 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_postcommentmodel_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcommentclapmodel',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claps', to='posts.postcommentmodel'),
        ),
    ]
