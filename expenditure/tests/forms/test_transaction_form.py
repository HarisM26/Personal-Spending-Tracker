from datetime import date, timedelta,datetime
from django import forms
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.models import Transaction, SpendingTransaction, IncomeTransaction, SpendingCategory, IncomeCategory, Limit, User
from decimal import Decimal
from expenditure.forms import IncomeTransactionForm, SpendingTransactionForm


class TransactionFormTestCase(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
              'expenditure/tests/fixtures/other_users.json']

    def setUp(self):

        self.category = SpendingCategory.objects.create(
            user = User.objects.get(email='johndoe@example.com'),
            name = 'test_category',
            #is_income=False,
            limit = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )

        self.category_2 = IncomeCategory.objects.create(
            user = User.objects.get(email='janedoe@example.com'),
            name = 'test2_category',
        )

        self.form_input = {
            'title': 'req_trans',
            'date': date.today(),
            'amount': 30.00,
            'spending_category': self.category.pk,
        }

        self.incoming_form_input = {
            'title': 'req_incoming_trans',
            'date': date.today(),
            'amount': 30.00,
            'income_category': self.category_2.pk,
        }
        
        self.image = SimpleUploadedFile('reciept.jpg', b'blablabla')

    def test_form_contains_required_fields(self):
        form = SpendingTransactionForm()
        self.assertIn('title', form.fields)
        self.assertIn('date', form.fields)
        self.assertIn('amount', form.fields)
    
    def test_incoming_form_contains_required_fields(self):
        form = IncomeTransactionForm()
        self.assertIn('title', form.fields)
        self.assertIn('date', form.fields)
        self.assertIn('amount', form.fields)

    def test_form_accepts_valid_input(self):
        form = SpendingTransactionForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_incoming_form_accepts_valid_input(self):
        form = IncomeTransactionForm(data=self.incoming_form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_rejects_blank_title(self):
        self.form_input['title'] = ''
        form = SpendingTransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_incoming_form_rejects_blank_title(self):
        self.incoming_form_input['title'] = ''
        form = IncomeTransactionForm(data=self.incoming_form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_date(self):
        self.form_input['date'] = ''
        form = SpendingTransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_incoming_form_rejects_blank_date(self):
        self.incoming_form_input['date'] = ''
        form = IncomeTransactionForm(data=self.incoming_form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_amount(self):
        self.form_input['amount'] = ''
        form = SpendingTransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_incoming_form_rejects_blank_amount(self):
        self.incoming_form_input['amount'] = ''
        form = IncomeTransactionForm(data=self.incoming_form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_incorrect_date(self):
        self.form_input['date'] = date.today() + timedelta(days=10)
        form = SpendingTransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_incoming_form_rejects_incorrect_date(self):
        self.incoming_form_input['date'] = date.today() + timedelta(days=10)
        form = IncomeTransactionForm(data=self.incoming_form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_notes(self):
        self.form_input['notes'] = 'some notes'
        form = SpendingTransactionForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_incoming_form_accepts_notes(self):
        self.incoming_form_input['notes'] = 'some notes'
        form = IncomeTransactionForm(data=self.incoming_form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_accepts_reciept(self):
        self.form_input['reciept'] = self.image
        form = SpendingTransactionForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    # def test_form_rejects_reciept(self):
    #     self.incoming_form_input['reciept'] = self.image
    #     form = IncomingForm(data=self.incoming_form_input)
    #     self.assertFalse(form.is_valid())
