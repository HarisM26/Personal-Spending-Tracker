from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.core.validators import MinValueValidator
from expenditure.choices import *


class Limit(models.Model):
    limit_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, validators=[
                                       MinValueValidator(Decimal('0.01'))])
    remaining_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(
        max_length=50, choices=LIMIT_STATUS, default='not reached')
    time_limit_type = models.CharField(
        max_length=7, choices=TIME_LIMIT_TYPE, default='weekly')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return str(self.limit_amount)

    @property
    def calc_90_percent_of_limit(self):
        return Decimal(self.limit_amount)*Decimal('0.90')
