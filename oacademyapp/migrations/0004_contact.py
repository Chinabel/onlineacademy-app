# Generated by Django 5.1.4 on 2025-01-03 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oacademyapp", "0003_youtubevideo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("message", models.TextField()),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
