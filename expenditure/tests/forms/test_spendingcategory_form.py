from datetime import date, timedelta, datetime
from django import forms
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.forms import *
from expenditure.models import Transaction, SpendingCategory, Limit, User
from decimal import Decimal

class SpendingCategoryFormTest(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
              'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.category = SpendingCategory.objects.create(
            user = User.objects.get(email='johndoe@example.com'),
            name = 'test_category',
            limit = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                remaining_amount = Decimal('10.00'),
                time_limit_type = 'weekly',
                start_date= date.today(),
                end_date= datetime.now() + timedelta(days=7)
            )
        )

        self.form_input = {
            'name':'Test_Category'
        }

    def test_form_contains_required_fields(self):
        form = SpendingCategoryForm()
        self.assertIn('name', form.fields)

    def test_form_accepts_valid_input(self):
        form = SpendingCategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_name(self):
        self.form_input['name'] = ''
        form = SpendingCategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_rejects_overlong_name(self):
        self.form_input['name'] = 'x' * 51
        form = SpendingCategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())