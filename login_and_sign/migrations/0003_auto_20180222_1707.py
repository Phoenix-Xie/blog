# Generated by Django 2.0.1 on 2018-02-22 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_and_sign', '0002_auto_20180219_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=50, verbose_name='密码'),
        ),
    ]
