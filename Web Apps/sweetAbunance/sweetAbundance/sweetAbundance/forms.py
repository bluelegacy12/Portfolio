from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from .models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    retype_password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email = models.EmailField(max_length=254, unique=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

class NameForm(forms.ModelForm):
    name = forms.CharField(label="Name", max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)
    retype_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password']

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField()
    text = models.TextField(null=False, max_length=1000)
    
    class Meta:
        model = Review
        fields = ['account', 'rating', 'text', 'product']
