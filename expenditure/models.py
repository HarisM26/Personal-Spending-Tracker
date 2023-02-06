from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    



class User(AbstractBaseUser):
  email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )

  
  first_name = models.CharField(
    max_length=30,
    blank=True,
    )

  last_name = models.CharField(
    max_length=150,
    blank=True,
    )

    
  REQUIRED_FIELDS = ('User',)


  objects =  UserManager()
  USERNAME_FIELD = 'email'



    
   


class Notification(models.Model):
  #user_receiver = models.ForeignKey(User,on_delete=models.CASCADE)
  title = models.CharField(max_length=50, blank= False)
  message = models.CharField(max_length = 500, blank = False)
  status = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)