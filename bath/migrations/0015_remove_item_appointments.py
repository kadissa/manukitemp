# Generated by Django 4.2 on 2024-05-13 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bath', '0014_alter_customer_email_alter_customer_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='appointments',
        ),
    ]