# Generated by Django 5.0 on 2025-05-31 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_alter_order_total_price_alter_orderitem_price_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ConsultationMessage',
        ),
    ]
