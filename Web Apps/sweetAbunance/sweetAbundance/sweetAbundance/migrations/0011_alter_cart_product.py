# Generated by Django 4.2.5 on 2024-04-17 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sweetAbundance', '0010_remove_cart_product_cart_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.JSONField(default={}),
        ),
    ]
