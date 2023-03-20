from django.test import TestCase
from django.urls import reverse
from expenditure.models.user import User
from expenditure.tests.helpers import reverse_with_next


class NotificationToggleTest(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.com')
        self.url = reverse('toggle_notification')

    def test_notification_toggle_url(self):
        self.assertEqual(self.url, '/settings/toggle_notification')

    def test_get_notification_toggle_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)
