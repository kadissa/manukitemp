# Generated by Django 4.2 on 2024-05-21 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bath', '0020_alter_product_options'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='product',
            index_together={('name', 'slug')},
        ),
    ]
