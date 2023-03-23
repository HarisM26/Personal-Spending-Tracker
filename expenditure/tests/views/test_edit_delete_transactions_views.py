from datetime import date, timedelta, datetime
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import User
from expenditure.models.limit import Limit
from decimal import Decimal


class EditAndDeleteTransactionsViews(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.category = SpendingCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name='test_category',
            limit=Limit.objects.create(
                limit_amount=Decimal('100.00'),
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )

        self.category_2 = IncomeCategory.objects.create(
            user=User.objects.get(email='janedoe@example.com'),
            name='test2_category',
        )

        self.transaction = SpendingTransaction.objects.create(
            title='req_trans',
            date=date.today(),
            amount=Decimal('30.00'),
            spending_category=self.category,
            is_current=True,
        )

        self.transaction_incoming = IncomeTransaction.objects.create(
            title='req_incomeing_trans',
            date=date.today(),
            amount=Decimal('10.00'),
            income_category=self.category_2,
        )

        self.transaction_input = {
            'title': 'req_trans',
            'date': date.today(),
            'amount': Decimal('80.00'),
            'spending_category': self.category.id,
            'is_current': True,
        }

        self.incoming_transaction_input = {
            'title': 'req_incomeing_trans',
            'date': date.today(),
            'amount': Decimal('60.00'),
            'income_category': self.category_2.id,
        }

        self.image = SimpleUploadedFile(
            'receipt.jpg', b'blablabla', content_type='image/jpeg')
        self.url = reverse('delete_spending', kwargs={'id': self.transaction.pk})
        self.url_2 = reverse('delete_income', kwargs={'id': self.transaction_incoming.pk})

    def test_edit_spending_details(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(f'/spending/edit/{self.transaction.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('edit_spending_transaction.html', (t.name for t in response.templates))

    def test_edit_incoming_details(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(f'/incomings/edit/{self.transaction_incoming.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('edit_income_transaction.html', (t.name for t in response.templates))

    def test_successful_edit_spending_details(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.post(f'/spending/edit/{self.transaction.pk}/', self.transaction_input)
        transaction = SpendingTransaction.objects.get(pk=self.transaction.pk)
        self.assertEqual(transaction.title, self.transaction_input['title'])
        self.assertEqual(transaction.date, self.transaction_input['date'])
        self.assertEqual(transaction.spending_category.pk, self.transaction_input['spending_category'])
        self.assertEqual(transaction.amount, Decimal('80.00'))
        self.assertEqual(response.status_code, 302)

    def test_successful_edit_incoming_details(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.post(f'/incomings/edit/{self.transaction_incoming.pk}/', self.incoming_transaction_input)
        transaction = IncomeTransaction.objects.get(pk=self.transaction_incoming.pk)
        self.assertEqual(transaction.title, self.incoming_transaction_input['title'])
        self.assertEqual(transaction.date, self.incoming_transaction_input['date'])
        self.assertEqual(transaction.income_category.pk, self.incoming_transaction_input['income_category'])
        self.assertEqual(transaction.amount, Decimal('60.00'))
        self.assertEqual(response.status_code, 302)

    def test_spending_limit_amount_change(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.post(f'/spending/edit/{self.transaction.pk}/', self.transaction_input)
        transaction = SpendingTransaction.objects.get(pk=self.transaction.pk)
        self.assertEqual(transaction.spending_category.limit.remaining_amount, Decimal('20.00'))

    def test_delete_spending_url(self):
        self.assertEqual(self.url, f'/spending/delete/{self.transaction.pk}/')

    def test_delete_incoming_url(self):
        self.assertEqual(self.url_2, f'/incomings/delete/{self.transaction_incoming.pk}/')

    def test_delete_spending_successfully(self):
        before_count = SpendingTransaction.objects.count()
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(self.url)
        after_count = SpendingTransaction.objects.count()
        self.assertEqual(after_count, before_count-1)
        response_url = reverse('spending')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)

    def test_delete_incoming_successfully(self):
        before_count = IncomeTransaction.objects.count()
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(self.url_2)
        after_count = IncomeTransaction.objects.count()
        self.assertEqual(after_count, before_count-1)
        response_url = reverse('incomings')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
