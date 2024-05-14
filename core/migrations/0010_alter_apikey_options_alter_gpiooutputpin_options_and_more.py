# Generated by Django 4.2.7 on 2023-12-24 20:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_rename_gpiopin_gpiooutputpin_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="apikey",
            options={"verbose_name": "Api Key", "verbose_name_plural": "Api Keys"},
        ),
        migrations.AlterModelOptions(
            name="gpiooutputpin",
            options={
                "verbose_name": "GPIO Output Pin",
                "verbose_name_plural": "GPIO Output Pins",
            },
        ),
        migrations.AlterModelOptions(
            name="numericallog",
            options={
                "verbose_name": "Numerical Log",
                "verbose_name_plural": "Numerical Logs",
            },
        ),
        migrations.AddField(
            model_name="gpiooutputpin",
            name="affects_variable",
            field=models.BooleanField(default=False, verbose_name="Affects Variable"),
        ),
    ]
