# Generated by Django 4.2.7 on 2023-11-28 11:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="device_id",
            field=models.UUIDField(
                default=uuid.uuid4, unique=True, verbose_name="Device ID"
            ),
        ),
    ]
