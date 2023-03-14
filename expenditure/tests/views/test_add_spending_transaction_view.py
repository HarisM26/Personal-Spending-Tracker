from datetime import date,timedelta,datetime
from django.test import TestCase
from django.urls import reverse
from expenditure.models import SpendingTransaction, SpendingCategory, Limit, User
from decimal import Decimal
from expenditure.forms import SpendingTransactionForm

class AddSpendingTransactionViews(TestCase):

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

        self.transaction_input = {
            'amount': Decimal('80.00'),
            'spending_category': self.category.id,
        }

        self.feed = reverse('feed')

    def test_transaction_urls(self):
        self.assertEqual(self.feed,'/feed/')