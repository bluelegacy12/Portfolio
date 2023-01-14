from django import forms
from .models import Performers
from django.contrib.auth.models import User

class NameForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    email = forms.CharField(label="Email", max_length=100)
    phone = forms.CharField(label="Phone", max_length=13, min_length=10)
    all_performers = Performers.objects.all()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']