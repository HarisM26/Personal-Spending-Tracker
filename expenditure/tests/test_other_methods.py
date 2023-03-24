from datetime import date, timedelta, datetime
from django.test import TestCase
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import User
from expenditure.models.limit import Limit
from expenditure.scheduler.scheduler import refresh_time_limit
from decimal import Decimal



class OtherMethodsTestCase(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.limit = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today() - timedelta(days=7),
                end_date=datetime.now() - timedelta(days=1)
            )
        self.category = SpendingCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name='test_category',
            limit=self.limit
        )
        self.limit_2 = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today()  - timedelta(days=7),
                end_date=datetime.now() - timedelta(days=1)
            )
        self.category_2 = SpendingCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name='test_category_2',
            limit=self.limit_2
        )
        
        self.user = User.objects.get(email='johndoe@example.com')

        self.transaction = SpendingTransaction.objects.create(
            title='req_trans',
            date=date.today(),
            amount=Decimal('30.00'),
            notes='Some notes',
            spending_category=self.category,
            is_current=True,
        )
        self.transaction_2 = SpendingTransaction.objects.create(
            title='req_trans_2',
            date=date.today(),
            amount=Decimal('30.00'),
            notes='Some notes',
            spending_category=self.category,
            is_current=True,
        )

    def test_is_current_is_off(self):
        refresh_time_limit()
        transaction = SpendingTransaction.objects.get(title='req_trans')
        transaction_2 = SpendingTransaction.objects.get(title='req_trans_2')
        self.assertFalse(transaction.is_current)
        self.assertFalse(transaction_2.is_current)
    