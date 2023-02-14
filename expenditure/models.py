from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .helpers import not_future
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
    )

  last_name = models.CharField(
    max_length=150,
    )

  id = models.AutoField(primary_key=True) 

  is_staff = models.BooleanField(default=False)
    
  is_active = models.BooleanField(default=True)

  TOGGLE_CHOICE=[('ON',('ON')),('OFF',('OFF'))]
  toggle_notification = models.CharField(max_length=3,choices=TOGGLE_CHOICE,default='ON')

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects =  UserManager()
  
  def __str__(self):   
    return self.email

  @property 
  def user_id(self):
    str(self.id) + self.first_name

class Limit(models.Model):
  LIMIT_STATUS=[('reached',('reached')),('not reached',('not reached')), ('approaching',('approaching'))]
  #TIME_LIMIT_TYPE=[('weekly',('weekly')),('monthly',('monthly')),('yearly',('yearly'))]

  limit_amount = models.DecimalField(max_digits=10,decimal_places=2,null=False, validators=[MinValueValidator(Decimal('0.01'))])
  remaining_amount = models.DecimalField(max_digits=10,decimal_places=2, default= 0.00)
  status = models.CharField(max_length=50, choices=LIMIT_STATUS, default='not reached')
  #time_limit_type = models.CharField(max_length=50, choices=TIME_LIMIT_TYPE, default='weekly')
  start_date = models.DateField()
  end_date = models.DateField()
 
  def __str__(self):
    return str(self.limit_amount)

  @property
  def calc_90_percent_of_limit(self):
    return Decimal(self.limit_amount)*Decimal('0.90')
  

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.email
  
  def __str__(self):
    return self.user.first_name
  
  def __str__(self):
    return self.user.last_name
  
  #def __str__(self):
   # return self.user.user_id


    
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
    limit = models.OneToOneField(Limit, on_delete=models.CASCADE)
    #slug = models.SlugField()
    #parent = models.ForeignKey('self',blank=True, null=True ,related_name='children')
    def __str__(self):
        return self.name

    # Used to create and save new instance of limit associated with this category
    def createLimit(category, limit_amount, **kwargs):
      Limit.objects.create(
        category=category,
        limit_amount=limit_amount,
        **kwargs
      )


# To get the outgoing transactions do: Category.spendings
class SpendingManager(models.Manager):
    def get_query_set(self):
      return super(SpendingManager, self).get_query_set().filter(
        category__is_income=False,
      )

# To get the incoming transactions do: Category.incomings
class IncomingManager(models.Manager):
    def get_query_set(self):
      return super(IncomingManager, self).get_query_set().filter(
        category__is_income=True,
      )

# To get all transactions do: Category.objects
class TransactionManager(models.Manager):
    def get_query_set(self):
      return super(TransactionManager, self).get_query_set()

class Transaction(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(validators=[not_future])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    reciept = models.ImageField(upload_to='', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name="transactions", on_delete=models.PROTECT)
    
    objects = TransactionManager()
    spendings = SpendingManager()
    incomings = IncomingManager()

    class Meta:
      ordering = ['-date',]
    
    def __str__(self):
        return 'desc: '+ self.title + ' -> $ ' + str(self.amount)

    class Meta:
        ordering = ['-date',]
  



  
