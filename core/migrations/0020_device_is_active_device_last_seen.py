# Generated by Django 5.0.6 on 2025-04-16 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_remove_profilesettings_mqtt_broker_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="device",
            name="is_active",
            field=models.BooleanField(default=False, verbose_name="Active Status"),
        ),
        migrations.AddField(
            model_name="device",
            name="last_seen",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Last Seen"),
        ),
    ]
