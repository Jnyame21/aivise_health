# Generated by Django 5.0 on 2025-05-28 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_consultationmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='contact_two',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='contact_two',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='license_issuer',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='license_number',
        ),
    ]
