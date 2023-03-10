# Generated by Django 4.1.5 on 2023-01-25 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getdata', '0004_alter_calltime_company_alter_rehearsalvenues_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calltime',
            name='date',
            field=models.DateField(default='1/1/2023 '),
        ),
        migrations.AlterField(
            model_name='calltime',
            name='end_time',
            field=models.TimeField(default='13:00 '),
        ),
        migrations.AlterField(
            model_name='calltime',
            name='start_time',
            field=models.TimeField(default='10:00 '),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(default='ex: Central Grand Opera', max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='roles',
            name='name',
            field=models.CharField(default='ex: Tosca ', max_length=128),
        ),
    ]
