from django.test import TestCase
from django import forms
from expenditure.forms import LimitForm
from expenditure.models import Limit
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import datetime, timedelta



class LimitFormTestCase(TestCase):
    """Unit tests for the LimitForm class."""

    def setUp(self):
        self.form_input = {
            'limit_amount': Decimal('1000.00'),
            'time_limit_type':'weekly',
        }

    def assert_limitform_is_valid(self):
        self.assertTrue(self.form_input.is_valid())

    def assert_limitform_is_invalid(self):
        with self.assertRaises(self.ValidationError):
            self.limit.full_clean()
    
    def test_form_has_necessary_fields(self):
        form = LimitForm()
        self.assertIn('limit_amount', form.fields)
        self.assertIn('time_limit_type', form.fields)
        self.assertIsInstance(form.fields['limit_amount'], forms.DecimalField)
    
    def test_form_is_valid(self):
        form = LimitForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_uses_form_validation(self):
        self.form_input['limit_amount'] = 0
        form = LimitForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_negative_limit_amount(self):
        self.form_input['limit_amount'] = -1000
        form = LimitForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_zero_limit_amount(self):
        self.form_input['limit_amount'] = 0.00
        form = LimitForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_limit_amount_with_more_than_10_digits(self):
        self.form_input['limit_amount'] = Decimal("123456789.10")
        form = LimitForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_accepts_limit_amount_with_10_digits(self):
        self.form_input['limit_amount'] = Decimal('12345678.10')
        form = LimitForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_rejects_limit_amount_with_more_than_2_decimal_places(self):
        self.form_input['limit_amount'] = Decimal("123.123")
        form = LimitForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_null_limit_amount(self):
        self.form_input['limit_amount'] = None
        form = LimitForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    #TODO: Add tests for start_date and end_date fields


