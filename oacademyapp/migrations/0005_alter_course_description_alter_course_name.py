# Generated by Django 5.1.4 on 2025-01-06 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oacademyapp", "0004_contact"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="description",
            field=models.TextField(verbose_name="Course Description"),
        ),
        migrations.AlterField(
            model_name="course",
            name="name",
            field=models.CharField(max_length=255, verbose_name="Course Name"),
        ),
    ]
