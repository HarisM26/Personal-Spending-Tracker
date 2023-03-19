from django.test import TestCase
from django.urls import reverse
from expenditure.models import User
from django.core import mail


class PasswordResetTest(TestCase):
    fixtures = ['expenditure/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('reset_password')
        self.user = User.objects.get(email='johndoe@example.com')

    def test_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_shown(self):
        response = self.client.post(self.url)
        self.assertTemplateUsed(response, 'password_reset.html')

    def test_password_reset_submit_with_valid_email(self):
        response = self.client.post(self.url, {'email': self.user.email})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_submit_with_invalid_email(self):
        response = self.client.post(
            self.url, {'email': 'thisemaildoesnotexist@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)
