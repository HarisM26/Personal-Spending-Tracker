from datetime import date, timedelta, datetime
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import User
from expenditure.models.limit import Limit
from decimal import Decimal


class BasicReportViews(TestCase):

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

        self.transaction = SpendingTransaction.objects.create(
            title='req_trans',
            date=date.today(),
            amount=Decimal('30.00'),
            spending_category=self.category,
            is_current=True,
        )

        self.image = SimpleUploadedFile(
            'receipt.jpg', b'blablabla', content_type='image/jpeg')

        self.url_reports = reverse('reports')

    def test_report_url(self):
        self.assertEqual(self.url_reports, '/reports/')

    def test_report_url_is_accessible(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response_reports = self.client.get(self.url_reports)
        self.assertEqual(response_reports.status_code, 200)
        self.assertIn('report.html', (t.name for t in response_reports.templates))

    def test_report_updates_with_date(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response_reports = self.client.post(self.url_reports, data={
            'from_date': date.today() - timedelta(days=5),
            'to_date': date.today(),
        })
        self.assertEqual(response_reports.status_code, 200)
        self.assertIn('report.html', (t.name for t in response_reports.templates))
