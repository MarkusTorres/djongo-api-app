# Generated by Django 4.1.13 on 2024-08-08 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Municipio",
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
                ("nombre", models.CharField(default="", max_length=50)),
                (
                    "precio",
                    models.DecimalField(decimal_places=2, max_digits=3, max_length=3),
                ),
            ],
        ),
    ]
