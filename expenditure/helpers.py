from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


def not_future(val):
    if val > date.today():
        raise ValidationError(_("Date should not be in the future."))
    elif not (isinstance(val, date)):
        raise ValidationError(_("Date should be in the right format: YYYY-MM-DD."))