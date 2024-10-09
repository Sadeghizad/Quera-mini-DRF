

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_alter_uservideointeraction_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservideointeraction',
            name='last_minute',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
