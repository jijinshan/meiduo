# Generated by Django 2.2.5 on 2020-12-23 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201220_2133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='creat_time',
            new_name='create_time',
        ),
    ]