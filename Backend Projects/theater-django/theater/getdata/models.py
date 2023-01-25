from django.db import models
import datetime
from django.urls import reverse
from django import forms

# Create your models here.
class Performers(models.Model):
    username = models.CharField(max_length=128, unique=True, null=False)
    name = models.CharField(max_length=128, null=False)
    email = models.CharField(max_length=128, unique=True, null=False)
    phone = models.CharField(max_length=128, unique=True, null=True, blank=True)
    public_profile = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('getdata:info', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class Company(models.Model):
    username = models.CharField(max_length=128, unique=True, null=False)
    name = models.CharField(max_length=128, unique=True, null=False)
    email = models.CharField(max_length=128, unique=True, null=False)
    performers = models.ManyToManyField(Performers, blank=True)

    def __str__(self):
        return self.name


class Shows(models.Model):
    title = models.CharField(max_length=128, null=False)
    rehearsal_start = models.DateField(null=False, default="1/1/2023")
    show_open = models.DateField(null=False, default="1/1/2023")
    director_id = models.ForeignKey(Performers, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
            return reverse('getdata:showinfo', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Roles(models.Model):
    name = models.CharField(max_length=128, null=False, default="ex: Tosca ")
    show_id = models.ForeignKey(Shows, on_delete=models.CASCADE)
    performer_id = models.ForeignKey(Performers, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
            return reverse('getdata:roleinfo', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name + " - from: " + self.show_id.title + " - performer: " + self.performer_id.name


class RehearsalVenues(models.Model):
    name = models.CharField(max_length=128, null=False, default="Main Rehearsal Hall")
    location = models.CharField(max_length=128, null=False, default="123 Fourth St.")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
            return reverse('getdata:venueinfo', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Conflicts(models.Model):
    performer_id = models.ManyToManyField(Performers)
    date_time = models.DateTimeField(null=False)
    endtime = models.DateTimeField(null=False)
    

class CallTime(models.Model):
    show_id_id = models.ForeignKey(Shows, on_delete=models.CASCADE)
    venue_id = models.ForeignKey(RehearsalVenues, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=False, default="1/1/2023 ")
    start_time = models.TimeField(null=False, default="10:00 ")
    end_time = models.TimeField(null=False, default="13:00 ")
    performers = models.ManyToManyField(Performers)
    notes = models.TextField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
            return reverse('getdata:callinfo', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.date) + ": " + str(self.start_time)  + " - " + str(self.end_time)

class Uploads(models.Model):
    name = models.CharField(max_length=128)
    details = models.TextField(null=True, blank=True)
    file = models.FileField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def get_absolute_url(self):
            return reverse('getdata:documents')

    def __str__(self):
        return self.name
