'''Unit test for the Sign Up Form'''
from django import forms
from django.test import TestCase
from django.contrib.auth.hashers import check_password
from expenditure.forms import SignUpForm
from expenditure.models import User


class SignUpFormTestCase(TestCase):
    fixtures = ['expenditure/tests/fixtures/default_user.json',
              'expenditure/tests/fixtures/other_users.json']
    def setUp(self):
        self.form_input = {
            'first_name': 'Will',
            'last_name': 'Smith',
            'email': 'willsmith@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
        }
    
        self.referrer_id = User.objects.get(email='johndoe@example.com').user_id

    # test that the form accepts input data

    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # test that the form has necessary fields
    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)

        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))

        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))

        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(
            password_confirmation_widget, forms.PasswordInput))

    # test that the form uses model validation
    def test_form_uses_model_validation(self):
        self.form_input['email'] = '@willsmith@gmail.com'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'hello123'
        self.form_input['password_confirmation'] = 'hello123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'HELLO123'
        self.form_input['password_confirmation'] = 'HELLO123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'helloHELLO'
        self.form_input['password_confirmation'] = 'helloHELLO'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = SignUpForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        user = User.objects.get(email='willsmith@example.org')
        self.assertEqual(user.first_name, 'Will')
        self.assertEqual(user.last_name, 'Smith')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)

    def test_reference_code_accepted(self):
        referrer = User.objects.get(email='johndoe@example.com')
        before_points = referrer.points
        self.form_input['reference_code'] = self.referrer_id
        form = SignUpForm(data=self.form_input)
        self.assertEqual(self.referrer_id, 'John@1')
        self.assertTrue(form.is_valid())
        form.save()
        #self.assertEqual(referrer.points, before_points+10)

    def test_reference_code_rejected_incorrect_format(self):
        self.form_input['reference_code'] = 'bhu@xdrt'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_reference_code_rejected_user_not_found(self):
        self.form_input['reference_code'] = self.referrer_id + '1'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
