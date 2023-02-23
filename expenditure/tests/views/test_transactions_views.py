from datetime import date,timedelta,datetime
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.models import Transaction, SpendingCategory, Limit, User
from decimal import Decimal

class TransactionViews(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
              'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.category = SpendingCategory.objects.create(
            user = User.objects.get(email='johndoe@example.com'),
            name = 'test_category',
            limit = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )

        self.category_2 = SpendingCategory.objects.create(
            user = User.objects.get(email='janedoe@example.com'),
            name = 'test2_category',
            limit = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )
        
        self.transaction = Transaction.objects.create(
            title = 'req_trans',
            date = date.today(),
            amount = Decimal('30.00'),
            category = self.category,
        )

        self.transaction_incoming = Transaction.objects.create(
            title = 'req_incomeing_trans',
            date = date.today(),
            amount = Decimal('10.00'),
            category = self.category_2,
        )

        self.transaction_input = {
            'title': 'transaction_test',
            'date': date.today(),
            'amount': Decimal('80.00'),
            'category': self.category.id,
        }

        self.incoming_transaction_input = {
            'title': 'incoming_transaction_test',
            'date': date.today(),
            'amount': Decimal('60.00'),
            'category': self.category_2.id,
        }

        self.image = SimpleUploadedFile('receipt.jpg', b'blablabla', content_type='image/jpeg')

        self.url_list_spendings = reverse('spending')
        self.url_list_incomings = reverse('incomings')
        self.url_add_transaction = reverse('add_transaction',args=[self.category.id])

    def test_transaction_urls(self):
        self.assertEqual(self.url_list_spendings,'/spending/')
        self.assertEqual(self.url_list_incomings,'/transactions/income/')
        self.assertEqual(self.url_add_transaction,f'/transactions/add/{self.category.id}/')
    
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
        self.client.login(email=self.category.user.email, password='Password123')
        before_count = Transaction.objects.count()
        response = self.client.post(self.url_add_transaction, self.transaction_input,follow=True)
        after_count = Transaction.objects.count()
        self.assertEqual(after_count, before_count+1)
        transaction = Transaction.objects.latest('created')
        self.assertEqual(self.category.user,transaction.category.user)
        response_url = reverse('spending')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    
    def test_add_incoming_transaction(self):
        self.client.login(email=self.category_2.user.email, password='Password123')
        before_count = Transaction.objects.count()
        response = self.client.post(self.url_add_transaction, self.incoming_transaction_input,follow=True)
        after_count = Transaction.objects.count()
        self.assertEqual(after_count, before_count+1)
        transaction = Transaction.objects.latest('created')
        response_url = reverse('spending')
        self.assertRedirects(response,response_url, status_code=302,target_status_code=200)
        self.assertEqual(transaction.title, self.incoming_transaction_input['title'])
        self.assertEqual(transaction.date, self.incoming_transaction_input['date'])
        self.assertEqual(transaction.amount, self.incoming_transaction_input['amount'])
        #self.assertEqual(transaction.category.pk, self.incoming_transaction_input['category'])

    