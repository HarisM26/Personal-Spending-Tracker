from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

"""Inspiration taken from https://groups.google.com/g/django-developers/c/LHnM_2jnZOM/m/8-oK6CXyEAAJ"""

def not_future(val):
    if val > date.today():
        raise ValidationError(_("Date should not be in the future."))
    elif not (isinstance(val, date)):
        raise ValidationError(_("Date should be in the right format: YYYY-MM-DD."))