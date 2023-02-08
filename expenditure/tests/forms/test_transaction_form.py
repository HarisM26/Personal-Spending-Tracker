from datetime import date, timedelta
from django import forms
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.forms import TransactionForm
from expenditure.models import Transaction, Category,User
from decimal import Decimal

class TransactionFormTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            user = User.objects.create(
                email='johndoe@email.com',
                first_name='John',
                last_name='Doe'
            ),
            name = 'test_category',
            limit = Decimal('50.00')
        )

        self.form_input = {
            'title': 'req_trans',
            'date': date.today(),
            'amount': 30.00,
            'category': self.category.pk,
        }
        
        self.image = SimpleUploadedFile('reciept.jpg', b'blablabla')

    def test_form_contains_required_fields(self):
        form = TransactionForm()
        self.assertIn('title', form.fields)
        self.assertIn('date', form.fields)
        self.assertIn('amount', form.fields)

    def test_form_accepts_valid_input(self):
        form = TransactionForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_rejects_blank_title(self):
        self.form_input['title'] = ''
        form = TransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_date(self):
        self.form_input['date'] = ''
        form = TransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_amount(self):
        self.form_input['amount'] = ''
        form = TransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_incorrect_date(self):
        self.form_input['date'] = date.today() + timedelta(days=10)
        form = TransactionForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_notes(self):
        self.form_input['notes'] = 'some notes'
        form = TransactionForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_accepts_is_income(self):
        self.form_input['is_income'] = True
        form = TransactionForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_accepts_reciept(self):
        self.form_input['reciept'] = self.image
        form = TransactionForm(data=self.form_input)
        self.assertTrue(form.is_valid())

