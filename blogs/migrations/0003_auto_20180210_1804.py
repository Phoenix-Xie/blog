# Generated by Django 2.0.1 on 2018-02-10 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20180210_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='passage',
            name='type1',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='passage',
            name='type2',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='passage',
            name='type3',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
