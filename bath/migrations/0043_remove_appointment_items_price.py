# Generated by Django 4.2 on 2024-06-06 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bath', '0042_alter_appointment_full_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='items_price',
        ),
    ]
