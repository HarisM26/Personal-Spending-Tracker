from django.test import TestCase
from django.urls import reverse


class PasswordResetTest(TestCase):

    def setUp(self):
        self.url = reverse('password_reset_complete')

    def test_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_shown(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'password_reset_complete.html')
