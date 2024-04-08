from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.urls import reverse
#from location_field.models.plain import PlainLocationField

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    text = models.TextField(null=False)
    video = models.FileField(upload_to='media/videos', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    photo = models.ImageField(default="default.jpg", upload_to='media/photos', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'pdf'])])

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profilePic = models.ImageField(default="default.jpg", upload_to='media/photos', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'pdf'])])
    bannerPic = models.ImageField(default="default.jpg", upload_to='media/photos', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'pdf'])])
    worksAt = models.CharField(max_length=255, null=True, blank=True)
    livesIn = models.CharField(max_length=255, null=True, blank=True)
    whereFrom = models.CharField(max_length=255, null=True, blank=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('profile')
    