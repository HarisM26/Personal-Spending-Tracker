from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date,datetime,timedelta
from django.conf import settings
from django.shortcuts import redirect
from decimal import Decimal
import expenditure.models

"""Inspiration taken from https://groups.google.com/g/django-developers/c/LHnM_2jnZOM/m/8-oK6CXyEAAJ"""

def not_future(val):
    if val > date.today():
        raise ValidationError(_("Date should not be in the future."))
    elif not (isinstance(val, date)):
        raise ValidationError(_("Date should be in the right format: YYYY-MM-DD."))

def create_notification(user,category_name,category_limit_obj,total):
  if total >= (category_limit_obj.calc_90_percent_of_limit) and total < Decimal(category_limit_obj.limit_amount):
    current_message = f'{category_name} category is close to its limit. Please consider reducing your spending'
  else:
    current_message = f'{category_name} category has reached its limit!'
  
  notification = expenditure.models.Notification.objects.create(
    user_receiver = user,
    title = 'About your limit',
    message = current_message 
  )
  return notification

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def get_end_date(limit_type):
  if limit_type == 'weekly':
      return datetime.date(datetime.now()) + timedelta(days=6)
  elif limit_type == 'monthly':
      return datetime.date(datetime.now()) + timedelta(days=27)
  else:
      return datetime.date(datetime.now()) + timedelta(days=364)
        