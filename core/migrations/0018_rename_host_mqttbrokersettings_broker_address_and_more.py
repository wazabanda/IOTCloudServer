# Generated by Django 5.0.6 on 2024-06-21 15:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_mqttbrokersettings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mqttbrokersettings',
            old_name='host',
            new_name='broker_address',
        ),
        migrations.RemoveField(
            model_name='mqttbrokersettings',
            name='profile_settings',
        ),
        migrations.RemoveField(
            model_name='mqttbrokersettings',
            name='topic',
        ),
        migrations.AlterField(
            model_name='mqttbrokersettings',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='mqttbrokersettings',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='mqttbrokersettings',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='MqttTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=255)),
                ('broker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='core.mqttbrokersettings')),
            ],
        ),
    ]