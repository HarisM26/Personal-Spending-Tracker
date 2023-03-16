from datetime import date, timedelta, datetime
from django.test import TestCase
from django.urls import reverse
from expenditure.models.transactions import SpendingTransaction
from expenditure.models.limit import Limit
from expenditure.models.categories import SpendingCategory
from expenditure.models.user import User
from decimal import Decimal
from expenditure.forms import QuickSpendingTransactionForm


class QuickTransactionViews(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.category = SpendingCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name='test_category',
            limit=Limit.objects.create(
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
        self.assertEqual(self.feed, '/feed/')

    # changed
    def test_transaction_urls_are_accessible(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(self.feed)

        self.assertEqual(response.status_code, 200)

        self.assertIn('feed.html', (t.name for t in response.templates))

    def test_add_transaction(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(self.feed)
        form = response.context['form']
        self.assertTrue(isinstance(form, QuickSpendingTransactionForm))
        self.assertFalse(form.is_bound)
        before_count = SpendingTransaction.objects.all().count()
        response = self.client.post(
            self.feed, self.transaction_input, follow=True)
        after_count = SpendingTransaction.objects.count()
        self.assertEqual(after_count, before_count+1)
        transaction = SpendingTransaction.objects.latest('created')
        self.assertEqual(self.category.user,
                         transaction.spending_category.user)
