from django.test import TestCase
from django import forms
from expenditure.forms import LimitForm
from expenditure.models import Limit


class LimitFormTestCase(TestCase):
    """Unit tests for the LimitForm class."""

    def setUp(self):
        self.form_input = {
            'limit_amount': 1000,
            'start_date': '2020-01-01',
            'end_date': '2020-01-02',
        }

    def assert_limitform_is_valid(self):
        self.assertTrue(is_valid())

    def assert_limitform_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.limit.full_clean()
    
    def test_form_has_necessary_fields(self):
        form = LimitForm()
        self.assertIn('limit_amount', form.fields)
        self.assertIn('start_date', form.fields)
        self.assertIn('end_date', form.fields)
        self.assertIsInstance(form.fields['limit_amount'], forms.DecimalField)
        self.assertIsInstance(form.fields['start_date'], forms.DateField)
        self.assertIsInstance(form.fields['end_date'], forms.DateField)
    
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
        self.form_input['limit_amount'] = 123456789.10
        form = LimitForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_accepts_limit_amount_with_10_digits(self):
        self.form_input['limit_amount'] = 12345678.90
        form = LimitForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_rejects_limit_amount_with_more_than_2_decimal_places(self):
        self.form_input['limit_amount'] = 123.123
        form = LimitForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_null_limit_amount(self):
        self.form_input['limit_amount'] = None
        form = LimitForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    #TODO: Add tests for start_date and end_date fields


