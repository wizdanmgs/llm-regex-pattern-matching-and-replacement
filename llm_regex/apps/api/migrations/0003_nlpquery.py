# Generated by Django 5.0.7 on 2024-07-30 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_remove_uploadedfile_uploaded_on"),
    ]

    operations = [
        migrations.CreateModel(
            name="NlpQuery",
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
                ("query", models.CharField(max_length=500)),
            ],
        ),
    ]