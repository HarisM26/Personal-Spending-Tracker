'''Unit test for the Sign Up View'''
from django.test import TestCase
from django.urls import reverse 
from django.contrib.auth.hashers import check_password
from expenditure.forms import SignUpForm
from expenditure.models import User

class SignUpFormTestCase(TestCase):
	def setUp(self):
		self.url = reverse('sign_up')
		self.form_input = {
		    'first_name': 'Will',
	        'last_name': 'Smith',
	        'email': 'willsmith@example.org',
	        'new_password': 'Password123',
	        'password_confirmation': 'Password123'
		}

	def test_sign_up_url(self):
		self.assertEqual(self.url,'/sign_up/')

	def test_get_sign_up(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'sign_up.html')
		form = response.context['form']
		self.assertTrue(isinstance(form, SignUpForm))
		self.assertFalse(form.is_bound)

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

	def successful_sign_up(self):
		before_count = User.objects.count()
		response = self.client.post(self.url, self.form_input, follow=True)
		after_count = User.objects.count()
		self.assertEqual(after_count, before_count + 1)
		response_url = reverse('about')
		self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
		self.assertTemplateUsed(response, 'about.html')
		user = User.objects.get(email = 'willsmith@example.org')
		self.assertEqual(user.first_name, 'will')
		self.assertEqual(user.last_name, 'smith')
		is_password_correct = check_password('Password123', user.password)
		self.assertTrue(is_password_correct)
