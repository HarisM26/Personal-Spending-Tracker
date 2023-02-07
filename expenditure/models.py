from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
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

class Transaction(models.model):

  def __str__(self):
    return "Transaction"

class Limit(models.model):

  def __str__(self):
    return "Limit"

class Category(models.Model):

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  # Each category has one spending limit, and that spending limit belongs to one category
  category_limit = models.OneToOneField(Limit, on_delete=models.CASCADE)
  transactions_total = models.DecimalField(max_digits=20,decimal_places=2)

  # Set the spending limit for this category
  def setLimit(self, limitAmount):
    self.category_limit.limit_amount = limitAmount

  # Update spent amount in category_limit
  def updateSpentAmountInLimit(self, amount):
    self.category_limit.spent_amount = amount

  # Set the total amount form all transaction in this category
  def setTotal(self):
    self.transactions_total = 0
    for transaction in Transaction.objects.filter(category=self):
      self.transactions_total += transaction.amount
    self.updateSpentAmountInLimit(self.transactions_total)
    
  # Adding to total when new transaction belonging to this category is created.
  def addToTotal(self, amount):
    self.transactions_total += amount
    self.updateSpentAmountInLimit(self.transactions_total)

  # Returns one of: reached, not reached or approaching 
  def getLimitStatus(self):
    return self.category_limit.status

  # Return total of all transactions in category
  def getTotal(self):
    return self.transactions_total

  def __str__(self):
    return self.name


class Transaction(models.Model):
    description = models.CharField(max_length=50,)
    amount = models.DecimalField(max_digits= 10, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,)

    def __str__(self):
        return 'desc: '+ self.description + ' -> $ ' + str(self.amount)
