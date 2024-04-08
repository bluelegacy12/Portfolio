# Generated by Django 4.2.5 on 2023-10-30 23:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trans_comm', '0005_alter_account_livesin_alter_account_occupation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='bannerPic',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='media/photos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='account',
            name='profilePic',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='media/photos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'pdf'])]),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='media/photos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'pdf'])]),
        ),
    ]
