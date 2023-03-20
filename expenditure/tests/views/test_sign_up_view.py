'''Unit test for the Sign Up View'''
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from expenditure.forms import SignUpForm
from expenditure.models import User, SpendingCategory
from expenditure.tests.helpers import LogInTester
from django.core import mail


class SignUpViewTestCase(TestCase, LogInTester):

    fixtures = ['expenditure/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'first_name': 'Will',
            'last_name': 'Smith',
            'email': 'willsmith@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123'
        }
        self.user = User.objects.get(email='johndoe@example.com')

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_get_sign_up_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_unsuccessful_sign_up(self):
        self.form_input['email'] = '@willsmith@example.org'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_sign_up(self):
        categories_before_count = SpendingCategory.objects.count()
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        user = User.objects.get(email='willsmith@example.org')
        self.assertEqual(user.first_name, 'Will')
        self.assertEqual(user.last_name, 'Smith')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        categories_after_count = SpendingCategory.objects.count()
        self.assertEqual(categories_after_count, categories_before_count + 4)
        categories = SpendingCategory.objects.all()
        self.assertFalse(categories[0].is_not_default)
        email = mail.outbox[0]
        self.assertEqual(email.to, ['willsmith@example.com'])
        self.assertEqual(email.subject, 'Welcome to Void Money Tracker')
