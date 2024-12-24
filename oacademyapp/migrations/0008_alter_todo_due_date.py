# Generated by Django 4.2.3 on 2024-12-18 12:26

from datetime import datetime, timezone
from django.utils import timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oacademyapp", "0007_alter_todo_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todo",
            name="due_date",
            field=models.DateTimeField(default=timezone.now),
        ),
    ]
