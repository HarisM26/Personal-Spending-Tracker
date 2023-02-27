'''Unit test for the Log Out View'''
from django.test import TestCase
from django.urls import reverse 
from expenditure.models import User
from expenditure.tests.helpers import LogInTester


class LogOutViewTestCase(TestCase, LogInTester):
    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.create_user(first_name = 'Will',
            last_name = 'Smith',
            email = 'willsmith@example.org',
            password = 'Password123',
            is_active = True,
    	)
    	
    def test_log_out_url(self):
    	self.assertEqual(self.url,'/log_out/')
    
    def test_get_log_out(self):
    	self.client.login(
            email = 'willsmith@example.org',
            password = 'Password123'
        )
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertFalse(self._is_logged_in())
