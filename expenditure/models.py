from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import datetime, date, timedelta
from decimal import Decimal
from django.core.validators import MinValueValidator


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
      extra_fields.setdefault("is_staff", True)
      extra_fields.setdefault("is_superuser", True)
      extra_fields.setdefault("is_active", True)

      if extra_fields.get("is_staff") is not True:
          raise ValueError(_("Superuser must have is_staff=True."))
      if extra_fields.get("is_superuser") is not True:
          raise ValueError(_("Superuser must have is_superuser=True."))
      return self.create_user(email, password, **extra_fields)

    



class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(_("email address"),
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

  is_staff = models.BooleanField(default=False)
    
  is_active = models.BooleanField(default=True)

    
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects =  UserManager()
  

def __str__(self):
  return self.email

    
class Notification(models.Model):
    STATUS_CHOICE=[('unread',('unread')),('read',('read'))]
    user_receiver = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    message = models.CharField(max_length = 1200)
    status = models.CharField(max_length=6,choices=STATUS_CHOICE,default= 'unread')
    time_created = models.TimeField(auto_now_add=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created','-time_created']
    
    def __str__(self):
        return self.message


class Category(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  is_income = models.BooleanField(default=False)

  # Used to create and save new instance of limit associated with this category
  def createLimit(category, limit_amount, **kwargs):
    Limit.objects.create(
      category=category,
      limit_amount=limit_amount,
      **kwargs
    )

  def __str__(self):
    return self.name


    
class Limit(models.Model):
  LIMIT_STATUS=[('reached',('reached')),('not reached',('not reached')), ('approaching',('approaching'))]
  TIME_LIMIT_TYPE=[('weekly',('weekly')),('monthly',('monthly')),('yearly',('yearly'))]

  # To access limit using category object, just do category.limit and vice versa
  category = models.OneToOneField(Category, null=True, blank=True, on_delete=models.PROTECT)
  limit_amount = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
  # Fields with default values
  spent_amount = models.DecimalField(max_digits=10,decimal_places=2, default=Decimal('0.00'))
  status = models.CharField(max_length=50, choices=LIMIT_STATUS, default='not reached')
  time_limit_type = models.CharField(max_length=50, choices=TIME_LIMIT_TYPE, default='weekly')
  start_date = models.DateField(default=date.today)
  end_date = models.DateField(default=date.today() + timedelta(weeks=1))

  def update_status(self):
    used_percent = self.get_percentage_of_limit_used()
    if used_percent >= 1.0:
      self.status = 'reached'
    elif used_percent >= 0.9:
      self.status = 'approaching'
    else:
      self.status ='not reached'
  
  def get_percentage_of_limit_used(self):
    return self.spent_amount/self.limit_amount

  # Return the amount spent from limit
  def getSpentAmount(self):
    return self.spent_amount

  # Return the currently set limit amount
  def getLimitAmount(self):
    return self.limit_amount

  # Set the spending limit
  def setLimitAmount(self, limitAmount):
    if (limitAmount >= 0):
      self.limit_amount = limitAmount
    else:
      return -1

  # Set spent amount in limit to spentAmount
  def setSpentAmount(self, spentAmount):
    if(spentAmount >= 0):
      self.spent_amount = spentAmount
      self.save()
    else:
      return -1

  # Subtract spent amount in limit by spentAmount
  def subtractSpentAmount(self, spentAmount):
    if(spentAmount >= 0):
      self.spent_amount -= spentAmount
      self.save()
    else:
      return -1

  # Add spent amount in limit by spentAmount
  def addSpentAmount(self, spentAmount):
    if(spentAmount >= 0):
      self.spent_amount += spentAmount
      self.save()
    else:
      return -1

  def save(self, *args, **kwargs):
    self.update_status()
    super(Limit, self).save(*args, **kwargs)


class Transaction(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    notes = models.TextField(blank=True)
    reciept = models.ImageField(upload_to='', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name="transactions", on_delete=models.PROTECT)

    def __str__(self):
        return 'desc: '+ self.title + ' -> $ ' + str(self.amount)

    class Meta:
        ordering = ['-date',]