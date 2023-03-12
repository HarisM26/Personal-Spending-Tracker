'''Unit test for the Sign Up Form'''
from django import forms
from django.test import TestCase
from django.contrib.auth.hashers import check_password
from expenditure.forms import NewForgottenPasswordForm


class TestNewForgottenPasswordFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
        }

    # test that the form accepts input data

    def test_valid_sign_up_form(self):
        form = NewForgottenPasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # test that the form has necessary fields
    def test_form_has_necessary_fields(self):
        form = NewForgottenPasswordForm()

        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))

        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(
            password_confirmation_widget, forms.PasswordInput))

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = NewForgottenPasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = NewForgottenPasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'Password'
        self.form_input['password_confirmation'] = 'Password'
        form = NewForgottenPasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())
