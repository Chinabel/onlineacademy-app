# Generated by Django 4.2.3 on 2023-07-11 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oacademyapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='is_finished',
            new_name='status',
        ),
    ]
