# Generated by Django 4.0 on 2022-01-31 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('store', '0003_alter_revievrating_product'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RevievRating',
            new_name='ReviewRating',
        ),
    ]
