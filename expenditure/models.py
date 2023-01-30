from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())
   


class Notification(models.Model):
  #user_receiver = models.ForeignKey(User,on_delete=models.CASCADE)
  title = models.CharField(max_length=50, blank= False)
  message = models.CharField(max_length = 500, blank = False)
  status = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)