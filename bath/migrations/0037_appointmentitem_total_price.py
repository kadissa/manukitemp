# Generated by Django 4.2 on 2024-06-01 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bath', '0036_remove_appointmentitem_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentitem',
            name='total_price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость'),
        ),
    ]
