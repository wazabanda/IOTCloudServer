# Generated by Django 4.2.7 on 2023-12-20 21:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_gpiopin_device"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="GPIOPin",
            new_name="GPIOOutputPin",
        ),
        migrations.AlterModelOptions(
            name="gpiooutputpin",
            options={
                "verbose_name": "GPIOOutputPin",
                "verbose_name_plural": "GPIOOutputPins",
            },
        ),
    ]
