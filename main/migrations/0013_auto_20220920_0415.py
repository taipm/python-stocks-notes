# Generated by Django 3.0.7 on 2022-09-20 04:15

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0012_vocabulary'),
    ]

    operations = [
        migrations.AddField(
            model_name='vocabulary',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 20, 4, 15, 32, 530975, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='vocabulary',
            name='enText',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='vocabulary',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vocabulary',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 20, 4, 15, 32, 530989, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='vocabulary',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vocabulary',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vocabulary',
            name='viText',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=200)),
                ('quantiy', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('hidden', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]