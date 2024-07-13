# Generated by Django 4.1.5 on 2023-04-13 20:53

from django.db import migrations, models
import django.db.models.deletion
import gdstorage.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CallTime",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                ("headline", models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=128, unique=True)),
                ("name", models.CharField(max_length=128, unique=True)),
                ("email", models.CharField(max_length=128, unique=True)),
                (
                    "logo",
                    models.FileField(
                        blank=True,
                        null=True,
                        storage=gdstorage.storage.GoogleDriveStorage(),
                        upload_to="calltime-uploads",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Performers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=128, unique=True)),
                ("first_name", models.CharField(max_length=128)),
                ("last_name", models.CharField(max_length=128)),
                ("email", models.CharField(max_length=128, unique=True)),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=128, null=True, unique=True
                    ),
                ),
                ("email_notifications", models.BooleanField(default=True)),
                ("public_profile", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Uploads",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("details", models.TextField(blank=True, null=True)),
                (
                    "file",
                    models.FileField(
                        storage=gdstorage.storage.GoogleDriveStorage(),
                        upload_to="calltime-uploads",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="getdata.company",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=128)),
                ("last_name", models.CharField(max_length=128)),
                ("email", models.CharField(max_length=128)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="getdata.company",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Shows",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128)),
                ("rehearsal_start", models.DateField(blank=True, null=True)),
                ("show_open", models.DateField()),
                (
                    "company",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="getdata.company",
                    ),
                ),
                (
                    "director_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="getdata.staff",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Roles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                (
                    "category",
                    models.ManyToManyField(
                        blank=True, null=True, to="getdata.category"
                    ),
                ),
                (
                    "performer_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="getdata.performers",
                    ),
                ),
                (
                    "show_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="getdata.shows"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RehearsalVenues",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                ("location", models.CharField(max_length=128)),
                (
                    "company",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="getdata.company",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuickCall",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField(blank=True, null=True)),
                ("details", models.CharField(blank=True, max_length=128, null=True)),
                (
                    "call",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="getdata.calltime",
                    ),
                ),
                (
                    "performers",
                    models.ManyToManyField(
                        blank=True, null=True, to="getdata.performers"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Conflicts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("start_time", models.TimeField(blank=True, null=True)),
                ("end_time", models.TimeField(blank=True, null=True)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="getdata.company",
                    ),
                ),
                (
                    "performer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="getdata.performers",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="company",
            name="performers",
            field=models.ManyToManyField(
                blank=True, null=True, to="getdata.performers"
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="getdata.company"
            ),
        ),
        migrations.AddField(
            model_name="calltime",
            name="company",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="getdata.company",
            ),
        ),
        migrations.AddField(
            model_name="calltime",
            name="performers",
            field=models.ManyToManyField(
                blank=True, null=True, to="getdata.performers"
            ),
        ),
        migrations.AddField(
            model_name="calltime",
            name="show_id_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="getdata.shows"
            ),
        ),
        migrations.AddField(
            model_name="calltime",
            name="staff",
            field=models.ManyToManyField(blank=True, null=True, to="getdata.staff"),
        ),
        migrations.AddField(
            model_name="calltime",
            name="venue_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="getdata.rehearsalvenues",
            ),
        ),
    ]