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

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    limit = models.DecimalField(max_digits= 10, decimal_places=2, verbose_name= 'category Limit')
    #slug = models.SlugField()
    #parent = models.ForeignKey('self',blank=True, null=True ,related_name='children')
    def __str__(self):
        return self.name
    """
    class Meta:
        #enforcing that there can not be two categories under a parent with same slug
        
        # __str__ method elaborated later in post.  use __unicode__ in place of
        
        # __str__ if you are using python 2

        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"    
        """ 

class Transaction(models.Model):
    description = models.CharField(max_length=50,)
    amount = models.DecimalField(max_digits= 10, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,)

    def __str__(self):
        return 'desc: '+ self.description + ' -> $ ' + str(self.amount)
