# Generated by Django 3.0.7 on 2021-09-17 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='answer',
        ),
    ]
