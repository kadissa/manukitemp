# Generated by Django 4.2 on 2024-05-07 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bath', '0012_alter_customer_email_alter_customer_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=60, null=True),
        ),
    ]