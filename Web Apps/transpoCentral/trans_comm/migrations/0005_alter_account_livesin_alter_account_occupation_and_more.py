# Generated by Django 4.2.5 on 2023-10-27 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trans_comm', '0004_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='livesIn',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='occupation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='whereFrom',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='worksAt',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]