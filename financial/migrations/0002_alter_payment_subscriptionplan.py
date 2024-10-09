

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='subscriptionplan',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='financial.subscriptionplan'),
            preserve_default=False,
        ),
    ]
