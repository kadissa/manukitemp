# Generated by Django 4.2 on 2024-05-14 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bath', '0016_appointment_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='bath.customer', verbose_name='Гость'),
        ),
    ]
