from datetime import date,timedelta,datetime
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.models import Transaction, Category, Limit, User
from decimal import Decimal
from expenditure.forms import IncomingForm, SpendingForm
from expenditure.views import get_total_transactions_by_date

class TransactionViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
                email='johndoe@email.com',
                first_name='John',
                last_name='Doe',
                password='1jk4uvdI0O',
        )

        self.category = Category.objects.create(
            user = self.user,
            name = 'test_category',
            is_income=False,
            limit = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )

        self.category_2 = Category.objects.create(
            user = self.user,
            name = 'test2_category',
            is_income=True,
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

        self.image = SimpleUploadedFile('reciept.jpg', b'blablabla', content_type='image/jpeg')

        self.url_reports = reverse('reports')

    # def test_total_transactions_by_date_only_spending(self):
    #     amount = get_total_transactions_by_date(self.user, date.today() - timedelta(days=5), date.today() + timedelta(days=1))
    #     self.assertEqual(amount.last(), self.transaction.amount)
    
    def test_report_url(self):
        self.assertEqual(self.url_reports,'/reports/')
    
    def test_report_url_is_accessible(self):
        self.client.login(email='johndoe@email.com', password='1jk4uvdI0O')
        response_reports = self.client.get(self.url_reports)
        self.assertEqual(response_reports.status_code, 200)
        self.assertIn('report.html', (t.name for t in response_reports.templates))
    
    def test_report_updates_with_date(self):
        self.client.login(email='johndoe@email.com', password='1jk4uvdI0O')
        response_reports = self.client.post(self.url_reports, data={
            'from_date': date.today() - timedelta(days=5),
            'to_date': date.today(),
        })
        self.assertEqual(response_reports.status_code, 200)
        self.assertIn('report.html', (t.name for t in response_reports.templates))


