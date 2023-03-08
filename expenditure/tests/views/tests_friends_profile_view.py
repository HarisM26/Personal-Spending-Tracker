from django.test import TestCase
from django.urls import reverse
from expenditure.models import User
from expenditure.tests import reverse_with_next

class ShowUserTest(TestCase):
 
    def setUp(self):
        self.user = User.objects.get(email= 'willsmith@example.org')
        self.url = reverse('friends_profile', kwargs={'email': self.email})
        
    
