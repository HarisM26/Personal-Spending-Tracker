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
from expenditure.models.categories import SpendingCategory, IncomeCategory


class Transaction(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(validators=[not_future])
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-date',]

    def __str__(self):
        return 'desc: ' + self.title + ' ->  £' + str(self.amount)


class SpendingTransaction(Transaction):
    spending_category = models.ForeignKey(
        SpendingCategory, related_name="transactions", null=True, on_delete=models.SET_NULL)
    receipt = models.ImageField(upload_to='', blank=True, null=True)
    is_current = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('transaction', kwargs={'id': self.pk})


class IncomeTransaction(Transaction):
    income_category = models.ForeignKey(
        IncomeCategory, related_name="transactions", null=True, on_delete=models.SET_NULL)
