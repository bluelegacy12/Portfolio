# Generated by Django 4.2.5 on 2023-10-14 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trans_comm', '0002_alter_post_user_alter_video_user_delete_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Hashtag',
        ),
    ]
