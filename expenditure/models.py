from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())
   


