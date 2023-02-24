from datetime import date,timedelta,datetime
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.models import Transaction, SpendingTransaction, IncomeTransaction, SpendingCategory, IncomeCategory, Limit, User
from decimal import Decimal
from expenditure.forms import IncomeTransactionForm, SpendingTransactionForm

class TransactionViews(TestCase):

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

        self.category_2 = IncomeCategory.objects.create(
            user = User.objects.get(email='janedoe@example.com'),
            name = 'test2_category',
        )
        
        self.transaction = SpendingTransaction.objects.create(
            title = 'req_trans',
            date = date.today(),
            amount = Decimal('30.00'),
            spending_category = self.category,
        )

        self.transaction_incoming = IncomeTransaction.objects.create(
            title = 'req_incomeing_trans',
            date = date.today(),
            amount = Decimal('10.00'),
            income_category = self.category_2,
        )

        self.transaction_input = {
            'title': 'transaction_test',
            'date': date.today(),
            'amount': Decimal('80.00'),
            'spending_category': self.category.id,
        }

        self.incoming_transaction_input = {
            'title': 'incoming_transaction_test',
            'date': date.today(),
            'amount': 60.00,
            'income_category': self.category_2.id,
        }

        self.image = SimpleUploadedFile('reciept.jpg', b'blablabla', content_type='image/jpeg')

        self.url_list_spendings = reverse('spending')
        self.url_list_incomings = reverse('list_incomings')
        self.url_add_transaction = reverse('add_spending_transaction',args=[self.category.id])
        self.url_add_income_transaction = reverse('add_income_transaction',args=[self.category_2.id])
        self.url_transaction = reverse('transaction', kwargs={'id': self.transaction.pk})

    def test_transaction_urls(self):
        self.assertEqual(self.url_list_spendings,'/spending/')
        self.assertEqual(self.url_list_incomings,'/transactions/income/')
        self.assertEqual(self.url_add_transaction,f'/transactions/add/{self.category.id}/')
        self.assertEqual(self.url_add_income_transaction,f'/transactions/add_income/{self.category_2.id}/')
        self.assertEqual(self.url_transaction,f'/transactions/{self.transaction.pk}/')
   
    #changed
    def test_transaction_urls_are_accessible(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response_list_spendings = self.client.get(self.url_list_spendings)
        response_list_incomings = self.client.get(self.url_list_incomings)
        response_add_transaction = self.client.get(self.url_add_transaction)
        response_add_income_transaction = self.client.get(self.url_add_income_transaction)
        response_transaction = self.client.get(self.url_transaction)

        self.assertEqual(response_list_spendings.status_code, 200)
        self.assertEqual(response_list_incomings.status_code, 200)
        self.assertEqual(response_add_transaction.status_code, 200)
        self.assertEqual(response_add_income_transaction.status_code, 200)
        self.assertEqual(response_transaction.status_code, 200)

        self.assertIn('spending.html', (t.name for t in response_list_spendings.templates))
        self.assertIn('incomings.html', (t.name for t in response_list_incomings.templates))
        self.assertIn('add_spending_transaction.html', (t.name for t in response_add_transaction.templates))
        self.assertIn('add_income_transaction.html', (t.name for t in response_add_income_transaction.templates))
        self.assertIn('transaction.html', (t.name for t in response_transaction.templates))
    
    #NOOOO
    # def test_add_transaction(self):
    #     self.client.login(email='johndoe@example.com', password='Password123')
    #     response = self.client.get(f'/transactions/add/{self.transaction.category.pk}/')
    #     form = response.context['create_transaction_form']
    #     self.assertTrue(isinstance(form, SpendingForm))
    #     self.assertFalse(form.is_bound)
    #     before_count = Transaction.objects.all().count()
    #     response = self.client.post(self.url_add_transaction, self.transaction_input)



    #NOOO
    #def test_transaction_urls_are_accessible(self):
        #response_list_spendings = self.client.get(self.url_list_spendings)
        #response_list_incomings = self.client.get(self.url_list_incomings)
        #response_add_transaction = self.client.get(self.url_add_transaction)
        #self.assertEqual(response_list_spendings.status_code, 302,200)
        #self.assertEqual(response_list_incomings.status_code, 302,200)
        #self.assertEqual(response_add_transaction.status_code, 302,200)
        #print(f'<<========== {response_list_spendings.templates}======>>')
        #self.assertIn('spending.html', (t.name for t in response_list_spendings.templates))
        #self.assertIn('incomings.html', (t.name for t in response_list_incomings.templates))
        #self.assertIn('add_transaction.html', (t.name for t in response_add_transaction.templates))
    
    def test_add_transaction(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(f'/transactions/add/{self.transaction.spending_category.pk}/')
        form = response.context['create_transaction_form']
        self.assertTrue(isinstance(form, SpendingTransactionForm))
        self.assertFalse(form.is_bound)
        before_count = SpendingTransaction.objects.all().count()
        response = self.client.post(self.url_add_transaction, self.transaction_input, follow=True)
        after_count = SpendingTransaction.objects.count()
        self.assertEqual(after_count, before_count+1)
        transaction = SpendingTransaction.objects.latest('created')
        self.assertEqual(self.category.user,transaction.spending_category.user)
        response_url = reverse('spending')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    
    def test_add_incoming_transaction(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(f'/transactions/add_income/{self.transaction_incoming.income_category.pk}/')
        form = response.context['create_transaction_form']
        self.assertTrue(isinstance(form, IncomeTransactionForm))
        self.assertFalse(form.is_bound)
        before_count = IncomeTransaction.objects.all().count()
        response = self.client.post(self.url_add_income_transaction, self.incoming_transaction_input, follow=True)
        after_count = IncomeTransaction.objects.count()
        self.assertEqual(after_count, before_count+1)
        transaction = IncomeTransaction.objects.latest('created')
        self.assertEqual(self.category_2.user,transaction.income_category.user)
        response_url = reverse('incomings')
        self.assertRedirects(response,response_url, status_code=302,target_status_code=200)
        self.assertEqual(transaction.title, self.incoming_transaction_input['title'])
        self.assertEqual(transaction.date, self.incoming_transaction_input['date'])
        self.assertEqual(transaction.amount, self.incoming_transaction_input['amount'])
        #self.assertEqual(transaction.category.pk, self.incoming_transaction_input['category'])

    