# Generated by Django 4.0.1 on 2022-01-27 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='vote',
        ),
    ]
