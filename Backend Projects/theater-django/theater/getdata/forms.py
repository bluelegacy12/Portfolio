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
    retype_password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(max_length=128)
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password']

class AddPerformerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class AddStaffForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    class Meta:
        model = User
        fields = ['name', 'email']
