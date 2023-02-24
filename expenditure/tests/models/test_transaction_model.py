from datetime import date, timedelta,datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from expenditure.models import Transaction, SpendingTransaction, IncomeTransaction, SpendingCategory, IncomeCategory, Limit, User
from decimal import *

class TestTransactionModel(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json']

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

        self.transaction = SpendingTransaction.objects.create(
            title = 'req_transaction',
            date = date.today(),
            amount = Decimal('30.00'),
            spending_category = self.category,
        )

        self.other_category = IncomeCategory.objects.create(
            user = User.objects.get(email='johndoe@example.com'),
            name = 'test2_category',
        )

        self.incoming = IncomeTransaction.objects.create(
            title = 'req_incoming',
            date = date.today(),
            amount = Decimal('30.00'),
            income_category = self.other_category,
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
        self.transaction.spending_category = None 
        self.assert_transaction_is_invalid()
    
    def test_rejects_incorrect_date(self):
        self.transaction.date = date.today() + timedelta(days=10)
        self.assert_transaction_is_invalid()
    
    def test_automated_creation_date(self):
        self.assertTrue(self.transaction.created)
        self.assertEqual(date.today().year, self.transaction.created.year)
        self.assertEqual(date.today().month, self.transaction.created.month)
        self.assertEqual(date.today().day, self.transaction.created.day)
    
    def test_unrequired_notes(self):
        self.transaction.notes = 'some notes' 
        self.assert_transaction_is_valid()
    
    def test_unrequired_reciept(self):
        self.transaction.reciept = self.image
        self.assert_transaction_is_valid()

    def test_str(self):
        self.assertEqual(str(self.transaction), f'desc: '+ self.transaction.title + ' ->  £' + str(self.transaction.amount))
    
    def test_get_absolute_url(self):
        response_url = reverse('transaction', kwargs={'id': self.transaction.pk})
        self.assertEqual(self.transaction.get_absolute_url(), response_url)
    
    def assert_incoming_is_valid(self):
        try:
            self.incoming.full_clean()
        except(ValidationError):
            self.fail("incoming should have passed")

    def assert_incoming_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.incoming.full_clean()
    
    def test_valid_incoming(self):
        self.assert_incoming_is_valid()
    
    def test_incoming_rejects_blank_title(self):
        self.incoming.title = '' 
        self.assert_incoming_is_invalid()
    
    def test_incoming_rejects_blank_date(self):
        self.incoming.date = None
        self.assert_incoming_is_invalid()
    
    def test_incoming_rejects_blank_amount(self):
        self.incoming.amount = None 
        self.assert_incoming_is_invalid()
    
    def test_incoming_rejects_blank_category(self):
        self.incoming.income_category = None 
        self.assert_incoming_is_invalid()
    
    def test_incoming_rejects_incorrect_date(self):
        self.incoming.date = date.today() + timedelta(days=10)
        self.assert_incoming_is_invalid()
    
    def test_incoming_automated_creation_date(self):
        self.assertTrue(self.incoming.created)
        self.assertEqual(date.today().year, self.incoming.created.year)
        self.assertEqual(date.today().month, self.incoming.created.month)
        self.assertEqual(date.today().day, self.incoming.created.day)

    def test_incoming_unrequired_notes(self):
        self.incoming.notes = 'some notes' 
        self.assert_incoming_is_valid()
    
    # def test_unrequired_reciept(self):
    #     self.spending.reciept = self.image
    #     self.assert_spending_is_valid()
