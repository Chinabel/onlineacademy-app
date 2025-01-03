# Generated by Django 5.1.4 on 2024-12-29 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("oacademyapp", "0002_delete_dictionary"),
    ]

    operations = [
        migrations.CreateModel(
            name="YouTubeVideo",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("url", models.URLField()),
                ("thumbnail_url", models.URLField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
