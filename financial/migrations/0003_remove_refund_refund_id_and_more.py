

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0002_alter_payment_subscriptionplan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refund',
            name='refund_id',
        ),
        migrations.AlterField(
            model_name='subscriptionpayment',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='financial.payment'),
        ),
    ]
