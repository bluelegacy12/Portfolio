# Generated by Django 4.2.5 on 2024-06-19 22:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sweetAbundance', '0014_account_id_alter_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
