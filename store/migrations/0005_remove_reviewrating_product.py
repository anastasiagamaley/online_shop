# Generated by Django 4.0 on 2022-01-31 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_revievrating_reviewrating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewrating',
            name='product',
        ),
    ]
