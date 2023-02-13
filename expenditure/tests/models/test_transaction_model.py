from datetime import date, timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.models import Transaction, Category, User, Limit
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
            limit = Limit.objects.create(limit_amount=Decimal('1000.00'),spent_amount=Decimal('0.00')),
            is_income=False,
        )

        self.transaction = Transaction.objects.create(
            title = 'req_transaction',
            date = date.today(),
            amount = Decimal('30.00'),
            category = self.category,
        )

        # self.other_category = Category.objects.create(
        #     user = User.objects.create(
        #         email='johndoe2@email.com',
        #         first_name='John',
        #         last_name='Doe'
        #     ),
        #     name = 'test2_category',
        #     limit = Decimal('60.00')
        # )

        # self.spending = Spending.objects.create(
        #     title = 'req_spending',
        #     date = date.today(),
        #     amount = Decimal('30.00'),
        #     category = self.category,
        # )
        # self.incoming = Incoming.objects.create(
        #     title = 'req_incoming',
        #     date = date.today(),
        #     amount = Decimal('30.00'),
        #     category = self.other_category,
        # )
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


    # def assert_spending_is_valid(self):
    #     try:
    #         self.spending.full_clean()
    #     except(ValidationError):
    #         self.fail("spending should have passed")
    
    # def assert_incoming_is_valid(self):
    #     try:
    #         self.incoming.full_clean()
    #     except(ValidationError):
    #         self.fail("incoming should have passed")

    # def assert_spending_is_invalid(self):
    #     with self.assertRaises(ValidationError):
    #         self.spending.full_clean()

    # def assert_incoming_is_invalid(self):
    #     with self.assertRaises(ValidationError):
    #         self.incoming.full_clean()

    # def test_valid_spending(self):
    #     self.assert_spending_is_valid()
    
    # def test_valid_incoming(self):
    #     self.assert_incoming_is_valid()

    # def test_rejects_blank_title(self):
    #     self.spending.title = '' 
    #     self.assert_spending_is_invalid()
    
    # def test_incoming_rejects_blank_title(self):
    #     self.incoming.title = '' 
    #     self.assert_incoming_is_invalid()

    # def test_rejects_blank_date(self):
    #     self.spending.date = None
    #     self.assert_spending_is_invalid()
    
    # def test_incoming_rejects_blank_date(self):
    #     self.incoming.date = None
    #     self.assert_incoming_is_invalid()

    # def test_rejects_blank_amount(self):
    #     self.spending.amount = None 
    #     self.assert_spending_is_invalid()
    
    # def test_incoming_rejects_blank_amount(self):
    #     self.incoming.amount = None 
    #     self.assert_incoming_is_invalid()
    
    # def test_rejects_blank_category(self):
    #     self.spending.category = None 
    #     self.assert_spending_is_invalid()
    
    # def test_incoming_rejects_blank_category(self):
    #     self.incoming.category = None 
    #     self.assert_incoming_is_invalid()
    
    # def test_rejects_incorrect_date(self):
    #     self.spending.date = date.today() + timedelta(days=10)
    #     self.assert_spending_is_invalid()
    
    # def test_incoming_rejects_incorrect_date(self):
    #     self.incoming.date = date.today() + timedelta(days=10)
    #     self.assert_incoming_is_invalid()
    
    # def test_automated_creation_date(self):
    #     self.assertTrue(self.spending.created)
    #     self.assertEqual(date.today().year, self.spending.created.year)
    #     self.assertEqual(date.today().month, self.spending.created.month)
    #     self.assertEqual(date.today().day, self.spending.created.day)
    
    # def test_incoming_automated_creation_date(self):
    #     self.assertTrue(self.incoming.created)
    #     self.assertEqual(date.today().year, self.incoming.created.year)
    #     self.assertEqual(date.today().month, self.incoming.created.month)
    #     self.assertEqual(date.today().day, self.incoming.created.day)

    # def test_unrequired_notes(self):
    #     self.spending.notes = 'some notes' 
    #     self.assert_spending_is_valid()
    
    # def test_incoming_unrequired_notes(self):
    #     self.incoming.notes = 'some notes' 
    #     self.assert_incoming_is_valid()
    
    # def test_unrequired_reciept(self):
    #     self.spending.reciept = self.image
    #     self.assert_spending_is_valid()
