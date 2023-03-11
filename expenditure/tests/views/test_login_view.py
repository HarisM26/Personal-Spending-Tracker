from django.test import TestCase
from django.urls import reverse
from expenditure.forms import LogInForm
from expenditure.models.user import User
from expenditure.tests.helpers import LogInTester, reverse_with_next
from django.contrib import messages


class LogInViewTestCase(TestCase, LogInTester):
    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(email='johndoe@example.com')

    def test_log_in_url(self):
        self.assertEqual(self.url, '/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(next)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_log_in_with_redirect(self):
        destination_url = reverse('feed')
        self.url = reverse_with_next('log_in', destination_url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(next, destination_url)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_log_in_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_unsuccesful_log_in(self):
        form_input = {'email': 'johndoe@example.com',
                      'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_email(self):
        form_input = {'email': '', 'password': 'Password123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_password(self):
        form_input = {'email': 'johndoe@example.com', 'password': ''}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_succesful_log_in(self):
        form_input = {'email': 'johndoe@example.com',
                      'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('feed')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_succesful_log_in_with_redirect(self):
        redirect_url = reverse('feed')
        form_input = {'email': 'johndoe@example.com',
                      'password': 'Password123', 'next': redirect_url}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = {'email': 'johndoe@example.com',
                      'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
