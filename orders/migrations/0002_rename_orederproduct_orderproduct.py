# Generated by Django 4.0 on 2022-01-23 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('store', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrederProduct',
            new_name='OrderProduct',
        ),
    ]
