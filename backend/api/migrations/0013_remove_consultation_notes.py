# Generated by Django 5.0 on 2025-05-30 01:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_staff_years_of_experience'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='notes',
        ),
    ]
