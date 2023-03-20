from datetime import date, timedelta, datetime
from django.test import TestCase
from expenditure.forms import *
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import User
from expenditure.models.limit import Limit
from decimal import Decimal


class SpendingCategoryEditMultiFormTestCase(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.category = SpendingCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name='test_category',
            limit=Limit.objects.create(
                limit_amount=Decimal('10.00'),
                remaining_amount=Decimal('10.00'),
                time_limit_type='weekly',
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )

        self.limit2 = Limit.objects.create(
            limit_amount=Decimal('100.00'),
            remaining_amount=Decimal('100.00'),
            time_limit_type='monthly',
            start_date=date.today(),
            end_date=datetime.now() + timedelta(days=7)
        )

        self.form_input = {
            'category-name': self.category.name,
            'limit-limit_amount': self.category.limit.limit_amount,
            'limit-time_limit_type': self.category.limit.time_limit_type
        }

    def test_form_contains_required_fields(self):
        form = SpendingCategoryEditMultiForm()
        self.assertIn('category-name', form.fields)
        self.assertIn('limit-limit_amount', form.fields)
        self.assertIn('limit-time_limit_type', form.fields)

    def test_form_accepts_valid_input(self):
        form = SpendingCategoryEditMultiForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_category_value(self):
        self.form_input['category-name'] = ''
        form = SpendingCategoryEditMultiForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_limit_value(self):
        self.form_input['limit-limit_amount'] = ''
        form = SpendingCategoryEditMultiForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_time_limit_type_value(self):
        self.form_input['limit-time_limit_type'] = ''
        form = SpendingCategoryEditMultiForm(data=self.form_input)
        self.assertFalse(form.is_valid())
