

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
