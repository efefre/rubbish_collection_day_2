# Generated by Django 3.0.7 on 2020-06-14 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='Miejscowość')),
                ('city_type', models.CharField(choices=[('gmina', 'Gmina'), ('miasto', 'Miasto')], default='gmina', max_length=10, verbose_name='Typ miejscowości')),
            ],
            options={
                'verbose_name': 'Miejscowość',
                'verbose_name_plural': 'Miejscowości',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Ulica')),
            ],
            options={
                'verbose_name': 'Ulica',
                'verbose_name_plural': 'Ulice',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='city_detail.City', verbose_name='Miasto')),
                ('rubbish_district', models.ManyToManyField(related_name='addresses', to='schedule.RubbishDistrict', verbose_name='Rejon')),
                ('street', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='city_detail.Street', verbose_name='Ulica')),
            ],
            options={
                'verbose_name': 'Adres odbioru odpadów',
                'verbose_name_plural': 'Adresy odbioru odpadów',
                'unique_together': {('city', 'street')},
            },
        ),
    ]
