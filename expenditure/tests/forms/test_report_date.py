from datetime import date, timedelta, datetime
from django.test import TestCase
from expenditure.forms import DateReportForm
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import User
from expenditure.models.limit import Limit
from decimal import Decimal


class DateFormTestCase(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):

        self.category = SpendingCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name='test_category',
            # is_income=False,
            limit=Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )
        self.transaction = SpendingTransaction.objects.create(
            title='req_trans',
            date=date.today(),
            amount=Decimal('30.00'),
            spending_category=self.category,
        )

        self.form_input = {
            'from_date': date.today() - timedelta(days=5),
            'to_date': date.today(),
        }

    def test_form_contains_required_fields(self):
        form = DateReportForm()
        self.assertIn('from_date', form.fields)
        self.assertIn('to_date', form.fields)

    def test_form_accepts_valid_input(self):
        form = DateReportForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_title(self):
        self.form_input['from_date'] = ''
        form = DateReportForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_date(self):
        self.form_input['to_date'] = ''
        form = DateReportForm(data=self.form_input)
        self.assertFalse(form.is_valid())
