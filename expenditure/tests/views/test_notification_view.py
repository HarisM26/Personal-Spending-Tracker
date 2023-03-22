from django.test import TestCase
from django.urls import reverse
from expenditure.models.user import User
from expenditure.tests.helpers import reverse_with_next
from expenditure.models.notification import Notification
from datetime import datetime, timedelta
from decimal import Decimal
from expenditure.models.categories import SpendingCategory
from expenditure.models.transactions import SpendingTransaction
from expenditure.models.limit import Limit


class NotificationViewTest(TestCase):
    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.com')
        self.notifications_url = reverse('notification_page')

        self.notification = Notification.objects.create(
            user_receiver=self.user,
            title='About your limit',
            message='category has reached its limit!',
        )
        self.view_notification_url = reverse(
            'view_selected_notification', args=[self.notification.id])

        self.category = SpendingCategory.objects.create(
            user=self.user,
            name='test_category',
            limit=Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=datetime.date(datetime.now()),
                end_date=datetime.now() + timedelta(days=7)
            )
        )
        self.url_add_transaction = reverse(
            'add_spending_transaction', args=[self.category.id])

    def test_notifications_url(self):
        self.assertEqual(self.notifications_url, '/notification_page/')

    def test_get_notifications_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.notifications_url)
        response = self.client.get(self.notifications_url)
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)

    def test_successful_notification_creation(self):
        before_count = Notification.objects.count()
        self.transaction = SpendingTransaction.objects.create(
            title='test transaction',
            spending_category=self.category,
            date=datetime.date(datetime.now()),
            amount=Decimal('10.00'),
        )
        after_count = Notification.objects.count()
        self.assertEqual(after_count, before_count + 1)
        notification = Notification.objects.latest('id')
        self.assertEqual(notification.title, 'About your limit')
        self.assertEqual(notification.status, 'unread')
        self.assertEqual(notification.message,
                         'test_category category has reached its limit!')

    def test_unsuccessful_notification_creation(self):
        before_count = Notification.objects.count()
        self.transaction = SpendingTransaction.objects.create(
            title='test transaction',
            spending_category=self.category,
            date=datetime.date(datetime.now()) + timedelta(days=1),
            amount=Decimal('-10.00'),
        )
        after_count = Notification.objects.count()
        self.assertEqual(after_count, before_count)

    def test_view_notification_url(self):
        self.assertEqual(self.view_notification_url,
                         f'/view_notification/{self.notification.id}')

    def test_get_view_notification_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.view_notification_url)
        response = self.client.get(self.view_notification_url)
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)

    def test_get_view_notification(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.view_notification_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_notification.html')
