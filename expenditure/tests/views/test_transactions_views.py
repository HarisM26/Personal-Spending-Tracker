from datetime import date, timedelta, datetime
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import User
from expenditure.models.limit import Limit
from decimal import Decimal
from expenditure.forms import IncomeTransactionForm, SpendingTransactionForm
from django.shortcuts import get_object_or_404


class TransactionViews(TestCase):

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

        self.image = SimpleUploadedFile(
            'receipt.jpg', b'blablabla', content_type='image/jpeg')

        self.category_2 = IncomeCategory.objects.create(
            user=User.objects.get(email='janedoe@example.com'),
            name='test2_category',
        )

        self.transaction = SpendingTransaction.objects.create(
            title='req_trans',
            date=date.today(),
            amount=Decimal('30.00'),
            notes='Some notes',
            receipt=self.image,
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
            'title': 'transaction_test',
            'date': date.today(),
            'amount': Decimal('80.00'),
            'spending_category': self.category.id,
            'is_current': True,
        }

        self.transaction_input_4_points = {
            'title': 'transaction_test',
            'date': date.today(),
            'amount': Decimal('80.00'),
            'notes': 'Some notes',
            'spending_category': self.category.id,
            'is_current': True,
        }

        self.transaction_input_4_points_2 = {
            'title': 'transaction_test',
            'date': date.today(),
            'amount': Decimal('80.00'),
            'notes': 'different',
            'spending_category': self.category.id,
            'receipt': self.image,
            'is_current': True,
        }

        self.transaction_input_5_points = {
            'title': 'transaction_test',
            'date': date.today(),
            'amount': Decimal('80.00'),
            'notes': 'Some notes',
            'spending_category': self.category.id,
            'receipt': self.image,
            'is_current': True,
        }

        self.edited_transaction = {
            'title': 'changed_title',
            'date': date.today(),
            'amount': Decimal('30.00'),
            'notes': 'changed',
            'receipt': self.image,
            'spending_category': self.category.id,
            'is_current': True,
        }

        self.incoming_transaction_input = {
            'title': 'incoming_transaction_test',
            'date': date.today(),
            'amount': 60.00,
            'income_category': self.category_2.id,
        }

        self.incoming_transaction_input_4_points = {
            'title': 'incoming_transaction_test',
            'date': date.today(),
            'amount': 60.00,
            'notes': 'Some notes',
            'income_category': self.category_2.id,
        }

        self.edited_incoming_transaction = {
            'title': 'changed_income_transaction',
            'date': date.today(),
            'amount': Decimal('100.00'),
            'notes': 'income',
            'income_category': self.category_2.id,
        }

        self.url_list_spendings = reverse('spending')
        self.url_list_incomings = reverse('list_incomings')
        self.url_add_transaction = reverse(
            'add_spending_transaction', args=[self.category.id])
        self.url_add_income_transaction = reverse(
            'add_income_transaction', args=[self.category_2.id])
        self.url_transaction = reverse(
            'transaction', kwargs={'id': self.transaction.pk})
        self.url_edit_transaction = reverse(
            'edit_spending', args=[self.transaction.id])
        self.url_edit_incoming_transaction = reverse(
            'edit_income', args=[self.transaction_incoming.pk])

    def test_transaction_urls(self):
        self.assertEqual(self.url_list_spendings, '/spending/')
        self.assertEqual(self.url_list_incomings, '/transactions/income/')
        self.assertEqual(self.url_add_transaction,
                         f'/transactions/add/{self.category.id}/')
        self.assertEqual(self.url_add_income_transaction,
                         f'/transactions/add_income/{self.category_2.id}/')
        self.assertEqual(self.url_transaction,
                         f'/transactions/{self.transaction.pk}/')
        self.assertEqual(self.url_edit_transaction,
                         f'/spending/edit/{self.transaction.id}/')
        self.assertEqual(self.url_edit_incoming_transaction,
                         f'/incomings/edit/{self.transaction_incoming.id}/')

    def test_transaction_urls_are_accessible(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response_list_spendings = self.client.get(self.url_list_spendings)
        response_list_incomings = self.client.get(self.url_list_incomings)
        response_add_transaction = self.client.get(self.url_add_transaction)
        response_add_income_transaction = self.client.get(
            self.url_add_income_transaction)
        response_transaction = self.client.get(self.url_transaction)

        self.assertEqual(response_list_spendings.status_code, 200)
        self.assertEqual(response_list_incomings.status_code, 200)
        self.assertEqual(response_add_transaction.status_code, 200)
        self.assertEqual(response_add_income_transaction.status_code, 200)
        self.assertEqual(response_transaction.status_code, 200)

        self.assertIn('spending.html',
                      (t.name for t in response_list_spendings.templates))
        self.assertIn('incomings.html',
                      (t.name for t in response_list_incomings.templates))
        self.assertIn('add_spending_transaction.html',
                      (t.name for t in response_add_transaction.templates))
        self.assertIn('add_income_transaction.html',
                      (t.name for t in response_add_income_transaction.templates))
        self.assertIn('transaction.html',
                      (t.name for t in response_transaction.templates))

    def test_add_transaction(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(
            f'/transactions/add/{self.transaction.spending_category.pk}/')
        form = response.context['create_transaction_form']
        self.assertTrue(isinstance(form, SpendingTransactionForm))
        self.assertFalse(form.is_bound)
        before_count = SpendingTransaction.objects.all().count()
        response = self.client.post(
            self.url_add_transaction, self.transaction_input, follow=True)
        after_count = SpendingTransaction.objects.count()
        self.assertEqual(after_count, before_count+1)
        transaction = SpendingTransaction.objects.latest('created')
        self.assertEqual(self.category.user,
                         transaction.spending_category.user)
        response_url = reverse('add_spending_transaction', args=[
                               self.transaction.spending_category.pk])
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)

    def test_add_incoming_transaction(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(
            f'/transactions/add_income/{self.transaction_incoming.income_category.pk}/')
        form = response.context['create_transaction_form']
        self.assertTrue(isinstance(form, IncomeTransactionForm))
        self.assertFalse(form.is_bound)
        before_count = IncomeTransaction.objects.all().count()
        response = self.client.post(
            self.url_add_income_transaction, self.incoming_transaction_input, follow=True)
        after_count = IncomeTransaction.objects.count()
        self.assertEqual(after_count, before_count+1)
        transaction = IncomeTransaction.objects.latest('created')
        self.assertEqual(self.category_2.user,
                         transaction.income_category.user)
        response_url = response_url = reverse('add_income_transaction', args=[
            self.transaction_incoming.income_category.pk])
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
        self.assertEqual(transaction.title,
                         self.incoming_transaction_input['title'])
        self.assertEqual(transaction.date,
                         self.incoming_transaction_input['date'])
        self.assertEqual(transaction.amount,
                         self.incoming_transaction_input['amount'])

    def test_transaction_returns_3_points_for_3_filled_fields(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(
            f'/transactions/add/{self.transaction.spending_category.pk}/')
        form = response.context['create_transaction_form']
        self.assertTrue(isinstance(form, SpendingTransactionForm))
        self.assertFalse(form.is_bound)
        response = self.client.post(
            self.url_add_transaction, self.transaction_input, follow=True)
        spending_transaction = SpendingTransaction.objects.latest('created')
        self.assertEqual(spending_transaction.get_points(), 3)
        response_url = reverse('add_spending_transaction', args=[
                               self.transaction.spending_category.pk])
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)

    def test_incoming_transaction_returns_3_points_for_3_filled_fields(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(
            f'/transactions/add_income/{self.transaction_incoming.income_category.pk}/')
        form = response.context['create_transaction_form']
        self.assertTrue(isinstance(form, IncomeTransactionForm))
        self.assertFalse(form.is_bound)
        response = self.client.post(
            self.url_add_transaction, self.incoming_transaction_input, follow=True)
        income_transaction = SpendingTransaction.objects.latest('created')
        self.assertEqual(income_transaction.get_points(), 3)
        response_url = reverse('add_spending_transaction', args=[
                               self.transaction.spending_category.pk])
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)

    def test_incoming_transaction_returns_4_points_for_4_filled_fields(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(
            f'/transactions/add_income/{self.transaction_incoming.income_category.pk}/')
        form = response.context['create_transaction_form']
        self.assertTrue(isinstance(form, IncomeTransactionForm))
        self.assertFalse(form.is_bound)
        response = self.client.post(
            self.url_add_transaction, self.incoming_transaction_input_4_points, follow=True)
        income_transaction = SpendingTransaction.objects.latest('created')
        self.assertEqual(income_transaction.get_points(), 4)
        response_url = reverse('add_spending_transaction', args=[
                               self.transaction.spending_category.pk])
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)


"""     def test_edit_transaction(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.post(self.url_edit_transaction, self.edited_transaction, follow=True)
        response_url = reverse('spending')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.title, self.edited_transaction['title'])
        self.assertEqual(self.transaction.amount, self.edited_transaction['amount'])
        self.assertEqual(self.transaction.date, self.edited_transaction['date'])
        self.assertEqual(self.transaction.notes, self.edited_transaction['notes'])
        self.assertTrue(self.transaction.receipt is not None)
        self.assertEqual(self.transaction.get_points(), 4)

    def test_edit_incoming_transaction(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.post(self.url_edit_incoming_transaction, self.edited_incoming_transaction, follow=True)
        incoming_transaction = IncomeTransaction.objects.get(id=self.transaction_incoming.pk)
        self.assertEqual(incoming_transaction.title, self.edited_incoming_transaction['title'])
        self.assertEqual(incoming_transaction.amount, self.edited_incoming_transaction['amount'])
        self.assertEqual(incoming_transaction.date, self.edited_incoming_transaction['date'])
        self.assertEqual(incoming_transaction.notes, self.edited_incoming_transaction['notes'])
        self.assertEqual(incoming_transaction.get_points(), 4)
        response_url = reverse('incomings')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200) """
