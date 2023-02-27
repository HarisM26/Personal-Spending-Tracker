from datetime import date, timedelta,datetime
from django import forms
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.forms import SpendingForm, IncomingForm
from expenditure.models import Transaction, Category, User, Limit
from decimal import Decimal

class TransactionFormTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            user = User.objects.create(
                email='johndoe@email.com',
                first_name='John',
                last_name='Doe',
            ),
            name = 'test_category',
            is_income=False,
            limit = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )

        self.category_2 = Category.objects.create(
            user = User.objects.create(
                email='johndoe2@email.com',
                first_name='John',
                last_name='Doe',
            ),
            name = 'test2_category',
            is_income=True,
            limit = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )

        self.form_input = {
            'title': 'req_trans',
            'date': date.today(),
            'amount': 30.00,
            'category': self.category.pk,
        }

        self.incoming_form_input = {
            'title': 'req_incoming_trans',
            'date': date.today(),
            'amount': 30.00,
            'category': self.category_2.pk,
        }
        
        self.image = SimpleUploadedFile('reciept.jpg', b'blablabla')

    def test_form_contains_required_fields(self):
        form = SpendingForm()
        self.assertIn('title', form.fields)
        self.assertIn('date', form.fields)
        self.assertIn('amount', form.fields)
    
    def test_incoming_form_contains_required_fields(self):
        form = IncomingForm()
        self.assertIn('title', form.fields)
        self.assertIn('date', form.fields)
        self.assertIn('amount', form.fields)

    def test_form_accepts_valid_input(self):
        form = SpendingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_incoming_form_accepts_valid_input(self):
        form = IncomingForm(data=self.incoming_form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_rejects_blank_title(self):
        self.form_input['title'] = ''
        form = SpendingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_incoming_form_rejects_blank_title(self):
        self.incoming_form_input['title'] = ''
        form = IncomingForm(data=self.incoming_form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_date(self):
        self.form_input['date'] = ''
        form = SpendingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_incoming_form_rejects_blank_date(self):
        self.incoming_form_input['date'] = ''
        form = IncomingForm(data=self.incoming_form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_amount(self):
        self.form_input['amount'] = ''
        form = SpendingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_incoming_form_rejects_blank_amount(self):
        self.incoming_form_input['amount'] = ''
        form = IncomingForm(data=self.incoming_form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_incorrect_date(self):
        self.form_input['date'] = date.today() + timedelta(days=10)
        form = SpendingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_incoming_form_rejects_incorrect_date(self):
        self.incoming_form_input['date'] = date.today() + timedelta(days=10)
        form = IncomingForm(data=self.incoming_form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_notes(self):
        self.form_input['notes'] = 'some notes'
        form = SpendingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_incoming_form_accepts_notes(self):
        self.incoming_form_input['notes'] = 'some notes'
        form = IncomingForm(data=self.incoming_form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_accepts_reciept(self):
        self.form_input['reciept'] = self.image
        form = SpendingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    # def test_form_rejects_reciept(self):
    #     self.incoming_form_input['reciept'] = self.image
    #     form = IncomingForm(data=self.incoming_form_input)
    #     self.assertFalse(form.is_valid())
