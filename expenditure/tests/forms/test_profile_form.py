from django import forms
from django.test import TestCase
from expenditure.forms import UpdateUserForm, SignUpForm
from expenditure.models import User


class UpdateUserFormTestCase(TestCase):
        def setUp(self):
            self.form_input = {
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'janedoe@example.org',
                
            }
            self.form_input_2 = {
            'first_name': 'Will',
            'last_name': 'Smith',
            'email': 'willsmith@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
        }


        def test_form_has_necessary_fields(self):
            form = UpdateUserForm()
            self.assertIn('first_name', form.fields)
            self.assertIn('last_name', form.fields)
            self.assertIn('email', form.fields)
            email_field = form.fields['email']
            self.assertTrue(isinstance(email_field, forms.EmailField))
        
        def test_valid_user_form(self):
            form = UpdateUserForm(data=self.form_input)
            self.assertTrue(form.is_valid())
        
        def test_form_uses_model_validation(self):
            self.form_input['email'] = 'bademail'
            form = UpdateUserForm(data=self.form_input)
            self.assertFalse(form.is_valid())
        
    
            
        """  def test_form_must_save_correctly(self):
            user = User.objects.filter(email='janedoe@example.org').first()
            form2 = UpdateUserForm(instance=user, data=self.form_input)
            form2.save()
            self.assertEqual(user.first_name, 'Jane')
            self.assertEqual(user.last_name, 'Doe')
            self.assertEqual(user.email, 'janedoe@example.org') """
            