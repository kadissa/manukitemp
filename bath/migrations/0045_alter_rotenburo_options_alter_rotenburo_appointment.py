# Generated by Django 4.2 on 2024-06-10 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bath', '0044_rotenburo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rotenburo',
            options={'verbose_name': 'Ротенбуро', 'verbose_name_plural': 'Ротенбуры'},
        ),
        migrations.AlterField(
            model_name='rotenburo',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rotenburos', to='bath.appointment', verbose_name='Заказ'),
        ),
    ]
