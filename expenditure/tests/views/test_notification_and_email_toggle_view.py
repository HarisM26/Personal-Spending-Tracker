from django.test import TestCase
from django.urls import reverse
from expenditure.models.user import User
from expenditure.tests.helpers import reverse_with_next
from expenditure.views.notification_views import toggle_notification


class NotificationToggleTest(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.com')
        self.url = reverse('toggle_notification')
        self.url_email = reverse('toggle_email')

    def test_notification_toggle_url(self):
        self.assertEqual(self.url, '/settings/toggle_notification')

    def test_get_notification_toggle_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url_email)
        response = self.client.get(self.url_email)
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)
    
    def test_toggle_notification(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        previous = self.user.toggle_notification
        response = self.client.get(self.url)
        now = User.objects.get(email='johndoe@example.com').toggle_notification
        self.assertNotEqual(previous, now)
        response_url = reverse('settings')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
    
    def test_toggle_notification_off(self):
        self.user.toggle_notification = 'OFF'
        self.user.save()
        self.client.login(email='johndoe@example.com', password='Password123')
        previous = self.user.toggle_notification
        response = self.client.get(self.url)
        now = User.objects.get(email='johndoe@example.com').toggle_notification
        self.assertNotEqual(previous, now)
        response_url = reverse('settings')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)

    def test_email_toggle_url(self):
        self.assertEqual(self.url_email, '/settings/toggle_email')

    def test_get_email_toggle_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)
    
    def test_toggle_email(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        previous = self.user.toggle_email
        response = self.client.get(self.url_email)
        now = User.objects.get(email='johndoe@example.com').toggle_email
        self.assertNotEqual(previous, now)
        response_url = reverse('settings')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
    
    def test_toggle_email_off(self):
        self.user.toggle_email = 'OFF'
        self.user.save()
        self.client.login(email='johndoe@example.com', password='Password123')
        previous = self.user.toggle_email
        response = self.client.get(self.url_email)
        now = User.objects.get(email='johndoe@example.com').toggle_email
        self.assertNotEqual(previous, now)
        response_url = reverse('settings')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
