from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from expenditure.helpers import not_future
from datetime import datetime, date, timedelta
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.urls import reverse
from expenditure.choices import *
from expenditure.models.limit import Limit
from expenditure.models.user import User


class SpendingCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    limit = models.OneToOneField(
        Limit, related_name='category', on_delete=models.CASCADE)
    # slug = models.SlugField()
    # parent = models.ForeignKey('self',blank=True, null=True ,related_name='children')
    # Reduce the remaining amount left of the spending limit

    def delete(self, *args, **kwargs):
        self.limit.delete()
        return super(SpendingCategory, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name


class IncomeCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
