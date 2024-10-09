

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0005_remove_uservideointeraction_interaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
