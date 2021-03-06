# Generated by Django 3.1 on 2020-08-20 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True, verbose_name='Data')),
            ],
            options={
                'verbose_name': 'Data',
                'verbose_name_plural': 'Daty',
            },
        ),
        migrations.CreateModel(
            name='RubbishType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nazwa frakcji')),
                ('mark_color', models.CharField(help_text='Podaj HEX zaczynająć od #. ', max_length=7, unique=True, verbose_name='Kolor zaznaczenia w kalendarzu')),
                ('css_name', models.CharField(help_text='Trzy litery związane z nazwą frakcji.', max_length=3, unique=True, verbose_name='Skrótowa nazwa frakcji')),
            ],
            options={
                'verbose_name': 'Frakcja',
                'verbose_name_plural': 'Frakcje śmieci',
            },
        ),
        migrations.CreateModel(
            name='ScheduleConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Calendar', max_length=255, verbose_name='Nazwa strony')),
                ('maintenance_mode', models.BooleanField(default=False, verbose_name='Przerwa techniczna')),
                ('year', models.IntegerField(default=2020, unique=True, verbose_name='Rok')),
                ('original_schedule', models.CharField(default='localhost', help_text='Link do harmonogramu opublikowanego na stronie UM', max_length=255, verbose_name='Link do harmonogramu')),
            ],
            options={
                'verbose_name': 'Konfiguracja harmonogramu',
            },
        ),
        migrations.CreateModel(
            name='RubbishDistrict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nazwa rejonu')),
                ('city_type', models.CharField(choices=[('gmina', 'Gmina'), ('miasto', 'Miasto')], default='gmina', max_length=10, verbose_name='Typ miejscowości')),
                ('date', models.ManyToManyField(blank=True, related_name='districts', to='schedule.Date', verbose_name='Daty')),
                ('rubbish_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='districts', to='schedule.rubbishtype', verbose_name='Frakcja')),
            ],
            options={
                'verbose_name': 'Rejon',
                'verbose_name_plural': 'Rejony odbioru odpadów',
                'unique_together': {('name', 'city_type', 'rubbish_type')},
            },
        ),
    ]
