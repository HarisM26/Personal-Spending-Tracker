'''Unit test for the Log In Form'''
from django import forms
from django.test import TestCase
from expenditure.forms import LogInForm


class LogInFormTestCase(TestCase):
	def setUp(self):
		self.form_input = {
		     'email': 'willsmith@example.org',
	         'password': 'Password123'
		}
	
	#test that the form has necessary fields
	def test_form_has_necessary_fields(self):
		form = LogInForm()
		self.assertIn('email',form.fields)
		self.assertIn('password',form.fields)
		password_field = form.fields['password']
		self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))
		
	#test that the form accepts input data
	def test_valid_log_in_form(self):
		form = LogInForm(data=self.form_input)
		self.assertTrue(form.is_valid())
		
	def test_form_rejects_blank_email(self):
		self.form_input['email'] = ''
		form = LogInForm(data=self.form_input)
		self.assertFalse(form.is_valid())
		
	def test_form_accepts_incorrect_email(self):
		self.form_input['email'] = 'hi'
		form = LogInForm(data=self.form_input)
		self.assertFalse(form.is_valid())
		
	def test_form_rejects_blank_password(self):
		self.form_input['password'] = ''
		form = LogInForm(data=self.form_input)
		self.assertFalse(form.is_valid())
		
	def test_form_accepts_incorrect_password(self):
		self.form_input['password'] = 'pwd'
		form = LogInForm(data=self.form_input)
		self.assertTrue(form.is_valid())   
