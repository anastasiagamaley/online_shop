# Generated by Django 4.0 on 2022-01-31 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_revievrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revievrating',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
    ]
