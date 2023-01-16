from django.db import models
import datetime
from django.urls import reverse

# Create your models here.
class Performers(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False)
    email = models.CharField(max_length=128, unique=True, null=False)
    phone = models.CharField(max_length=10, unique=True, null=False)

    def get_absolute_url(self):
        return reverse('getdata:info', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name + ', ' + self.email + ', ' + self.phone


class Shows(models.Model):
    title = models.CharField(max_length=128, unique=True, null=False)
    rehearsal_start = models.DateTimeField(null=False)
    show_open = models.DateTimeField(null=False)
    director_id = models.ForeignKey(Performers, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)

    def get_absolute_url(self):
            return reverse('getdata:showinfo', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title + " - directed by: " + self.director_id.name + " - opens: " + str(self.show_open)


class Roles(models.Model):
    name = models.CharField(max_length=128, null=False)
    show_id = models.ForeignKey(Shows, on_delete=models.CASCADE)
    performer_id = models.ForeignKey(Performers, on_delete=models.CASCADE)

    def get_absolute_url(self):
            return reverse('getdata:roleinfo', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name + " - from: " + self.show_id.title + " - performer: " + self.performer_id.name


class Scenes(models.Model):
    scene_name = models.CharField(max_length=128, unique=True, null=False)
    show_id = models.ForeignKey(Shows, on_delete=models.CASCADE)
    role_id = models.ManyToManyField(Roles)


class RehearsalVenues(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False)
    location = models.CharField(max_length=128, unique=True, null=False)
    show_id = models.ManyToManyField(Shows)


class Conflicts(models.Model):
    date_time = models.DateTimeField()
    performer_id = models.ManyToManyField(Performers)
