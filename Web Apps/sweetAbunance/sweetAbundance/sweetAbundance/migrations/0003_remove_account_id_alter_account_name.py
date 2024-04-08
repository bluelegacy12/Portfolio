# Generated by Django 4.2.5 on 2024-03-24 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sweetAbundance', '0002_account_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='id',
        ),
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(default=0, max_length=125, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
