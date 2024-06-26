# Generated by Django 4.2.7 on 2023-11-28 11:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import secrets
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Device",
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
                ("device_name", models.CharField(max_length=50, verbose_name="name")),
                (
                    "device_id",
                    models.UUIDField(default=uuid.uuid4, verbose_name="Device ID"),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "Device",
                "verbose_name_plural": "Devices",
            },
        ),
        migrations.CreateModel(
            name="NumericalLog",
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
                ("value", models.FloatField(default=0, verbose_name="Value")),
                (
                    "date_time",
                    models.DateTimeField(
                        default=datetime.datetime.utcnow,
                        null=True,
                        verbose_name="Date and time",
                    ),
                ),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.device",
                        verbose_name="Device",
                    ),
                ),
            ],
            options={
                "verbose_name": "NumericalLog",
                "verbose_name_plural": "NumericalLogs",
            },
        ),
        migrations.CreateModel(
            name="ApiKey",
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
                (
                    "key",
                    models.CharField(
                        default=secrets.token_urlsafe, max_length=64, verbose_name="Key"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "ApiKey",
                "verbose_name_plural": "ApiKeys",
            },
        ),
    ]
