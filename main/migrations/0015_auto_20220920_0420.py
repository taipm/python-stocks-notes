# Generated by Django 3.0.7 on 2022-09-20 04:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20220920_0418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vocabulary',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 20, 4, 20, 14, 665926, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 20, 4, 20, 14, 665938, tzinfo=utc)),
        ),
    ]
