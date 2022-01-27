# Generated by Django 4.0 on 2022-01-23 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_orederproduct_orderproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_total',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='tax',
            field=models.FloatField(null=True),
        ),
    ]