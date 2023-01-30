from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    username = models.CharField(max_length= 30,unique=True,validators = [RegexValidator(
            regex = r'^@\w{3,}$',
            message = 'Username must consist of @ followed by at least three alphanumerals'
    )]
        )
    first_name = models.CharField(max_length=30, )
    last_name = models.CharField(max_length=30, )
    email = models.EmailField(unique=True, )

class Notification(models.Model):
  STATUS_CHOICE=[('unread',('unread')),('read',('read'))]

  #user_receiver = models.ForeignKey(User,on_delete=models.CASCADE)
  title = models.CharField(max_length=300)
  message = models.CharField(max_length = 1200)
  status = models.CharField(max_length=6,choices=STATUS_CHOICE,default=1)
  time_created = models.TimeField(auto_now_add=True)
  date_created = models.DateField(auto_now_add=True)
  

