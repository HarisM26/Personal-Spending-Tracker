from datetime import date
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.models import Transaction, Category,User
from decimal import *

class TestTransactionModel(TestCase):

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
        self.transaction = Transaction.objects.create(
            title = 'req_trans',
            date = date.today(),
            amount = Decimal('30.00'),
            category = self.category,
        )
        self.image = SimpleUploadedFile('reciept.jpg', b'blablabla')

    def assert_transaction_is_valid(self):
        try:
            self.transaction.full_clean()
        except(ValidationError):
            self.fail("transaction should have passed")

    def assert_transaction_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.transaction.full_clean()

    def test_valid_transaction(self):
        self.assert_transaction_is_valid()

    def test_rejects_blank_title(self):
        self.transaction.title = '' 
        self.assert_transaction_is_invalid()

    def test_rejects_blank_date(self):
        self.transaction.date = None
        self.assert_transaction_is_invalid()

    def test_rejects_blank_amount(self):
        self.transaction.amount = None 
        self.assert_transaction_is_invalid()
    
    def test_rejects_blank_category(self):
        self.transaction.category = None 
        self.assert_transaction_is_invalid()
    
    def test_automated_creation_date(self):
        self.assertTrue(self.transaction.created)
        self.assertEqual(date.today().year, self.transaction.created.year)
        self.assertEqual(date.today().month, self.transaction.created.month)
        self.assertEqual(date.today().day, self.transaction.created.day)
    
    def test_default_is_income_false(self):
        self.assertFalse(self.transaction.is_income)

    def test_unrequired_notes(self):
        self.transaction.notes = 'some notes' 
        self.assert_transaction_is_valid()
    
    def test_unrequired_reciept(self):
        self.transaction.reciept = self.image
        self.assert_transaction_is_valid()

    def test_is_income_true(self):
        self.transaction.is_income = True
        self.assertTrue(self.transaction.is_income)
