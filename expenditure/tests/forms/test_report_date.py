from datetime import date, timedelta,datetime
from django import forms
from django.test import TestCase
from expenditure.forms import DateReportForm
from expenditure.models import Transaction, Category, User, Limit
from decimal import Decimal

class DateFormTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
                email='johndoe@email.com',
                first_name='John',
                last_name='Doe',
                password='1jk4uvdI0O',
            )
        self.category = Category.objects.create(
            user=self.user,
            name = 'test_category',
            is_income=False,
            limit = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )
        self.transaction = Transaction.objects.create(
            title = 'req_trans',
            date = date.today(),
            amount = Decimal('30.00'),
            category = self.category,
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
    