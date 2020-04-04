# Generated by Django 3.0.4 on 2020-04-04 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20200404_1719'),
        ('city_detail', '0003_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='rubbish_district',
            field=models.ManyToManyField(related_name='addresses', to='schedule.RubbishDistrict', verbose_name='Rejon'),
        ),
    ]
