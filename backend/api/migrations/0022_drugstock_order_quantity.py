# Generated by Django 5.0 on 2025-05-30 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_remove_order_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugstock',
            name='order_quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Quantity in Stock'),
        ),
    ]
