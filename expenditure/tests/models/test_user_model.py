'''Unit test for the User Model'''
from django.core.exceptions import ValidationError
from django.test import TestCase
from expenditure.models import User

class UserModelTestCase(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.com')
        
    #tests for user validity
    def test_valid_user(self):
        self._assert_user_is_valid()
         
    #tests for the first name
    def test_first_name_cannot_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()
        
    def test_first_name_can_already_exist(self):
        second_user = second_user = User.objects.get(email='janedoe@example.com')
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid() 
        
    def test_first_name_cannot_be_over_30_characters(self):
        self.user.first_name = 'x' * 30
        self._assert_user_is_invalid() 
        
    def test_first_name_can_be_up_to_30_characters(self):
        self.user.first_name = 'x' * 30
        self._assert_user_is_valid() 
        
    def test_first_name_cannot_be_over_30_characters(self):
        self.user.first_name = 'x' * 31
        self._assert_user_is_invalid() 
            
    #tests for the last name
    def test_last_name_cannot_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()
        
    def test_last_name_can_already_exist(self):
        second_user = User.objects.get(email='janedoe@example.com')
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid() 
        
    def test_last_name_can_be_up_to_150_characters(self):
        self.user.last_name = 'x' * 150
        self._assert_user_is_valid() 
        
    def test_last_name_cannot_be_over_150_characters(self):
        self.user.last_name = 'x' * 151
        self._assert_user_is_invalid() 

    #tests for the email
    def test_email_cannot_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()
        
    def test_email_must_be_unique(self):
        second_user = second_user = User.objects.get(email='janedoe@example.com')
        self.user.email = second_user.email
        self._assert_user_is_invalid() 
        
    def test_email_cannot_be_over_255_characters(self):
        self.user.email = 'x' * 256
        self._assert_user_is_invalid()  
        
    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()  
        
    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self._assert_user_is_invalid() 
      
    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid() 
        
    def test_email_must_not_contain_multiple_at_symbols(self):
        self.user.email = 'johndoe@@example.org'
        self._assert_user_is_invalid() 	      
    	      
    def test_toggle_notification(self):
        self.assertTrue(self.user.toggle_notification, 'ON')
        self.user.toggle_notification = 'OFF'
        self.assertTrue(self.user.toggle_notification, 'OFF')

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
