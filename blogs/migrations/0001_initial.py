# Generated by Django 2.0.1 on 2018-02-05 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login_and_sign', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login_and_sign.User')),
            ],
        ),
    ]
