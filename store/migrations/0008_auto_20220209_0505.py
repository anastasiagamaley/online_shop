# Generated by Django 3.2.9 on 2022-02-09 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_productgallery_options_alter_product_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviewrating',
            options={'ordering': ('created_date',)},
        ),
        migrations.AddField(
            model_name='reviewrating',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.reviewrating'),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='rating',
            field=models.FloatField(default=None),
        ),
    ]