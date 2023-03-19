from django.test import TestCase
from django.urls import reverse
from expenditure.models import User
from django.core import mail


class PasswordResetTest(TestCase):

    def setUp(self):
        self.url = reverse('password_reset_done')

    def test_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_shown(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'password_reset_sent.html')
