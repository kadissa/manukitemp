# Generated by Django 4.2 on 2024-05-28 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bath', '0030_alter_appointment_full_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Цена'),
        ),
    ]
