# Generated by Django 3.1 on 2020-08-22 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_scheduleconfiguration_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleconfiguration',
            name='gtm_number',
            field=models.CharField(default='empty_number', max_length=20, verbose_name='Identyfikator kontenera GTM'),
        ),
    ]
