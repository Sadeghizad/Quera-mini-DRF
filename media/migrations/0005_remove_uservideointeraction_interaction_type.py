

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0004_alter_uservideointeraction_last_minute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uservideointeraction',
            name='interaction_type',
        ),
    ]
