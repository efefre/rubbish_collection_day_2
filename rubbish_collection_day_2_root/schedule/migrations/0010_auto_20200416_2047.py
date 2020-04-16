# Generated by Django 3.0.4 on 2020-04-16 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_rubbishtype_css_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rubbishtype',
            name='css_name',
            field=models.CharField(help_text='Trzy litery związane z nazwą frakcji.', max_length=3, unique=True, verbose_name='Skrótowa nazwa frakcji'),
        ),
    ]
