from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

class Account(models.Model):
    name = models.CharField(max_length=125, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True)
    points = models.IntegerField(default=0)
    referredBy = models.CharField(max_length=6, null=True, blank=True)
    referCode = models.CharField(max_length=6, unique=True)

class Product(models.Model):
    name = models.CharField(max_length=125, unique=True, primary_key=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    photo = models.ImageField(upload_to="static/images/", default="static/images/noImage.png" )
    discount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def get_absolute_url(self):
            return reverse('product', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.name

class Flavor(models.Model):
    name = models.CharField(max_length=125, unique=True)
    color = models.CharField(max_length=125)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Review(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=5, validators=[MaxValueValidator(5), MinValueValidator(1)])
    text = models.TextField(null=False, max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

