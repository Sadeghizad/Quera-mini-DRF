# Generated by Django 5.1.1 on 2024-10-08 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_uservideointeraction_last_minute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservideointeraction',
            name='last_minute',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
