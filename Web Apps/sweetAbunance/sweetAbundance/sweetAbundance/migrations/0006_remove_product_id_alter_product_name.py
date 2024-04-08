# Generated by Django 4.2.5 on 2024-04-03 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sweetAbundance', '0005_review_product_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='id',
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=125, primary_key=True, serialize=False, unique=True),
        ),
    ]
