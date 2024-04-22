# Generated by Django 4.2.7 on 2024-04-16 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bath', '0007_item_created_at_item_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appointment',
            options={'verbose_name': 'Запись', 'verbose_name_plural': 'Бронирования'},
        ),
        migrations.AlterField(
            model_name='appointment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bath.customer', verbose_name='Гость'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=60, null=True),
        ),
        migrations.DeleteModel(
            name='Service',
        ),
    ]
