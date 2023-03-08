from django.test import TestCase
from django.urls import reverse
from expenditure.models import User
from expenditure.tests import reverse_with_next

class ShowUserTest(TestCase):
 
    def setUp(self):
        self.user = User.objects.get(email= 'willsmith@example.org')
        self.followee = User.objects.get(email= 'willowsmith@example.org')
        self.url = reverse('friends_toggle', kwargs={'email': self.followee.id})
        
    def test_follow_toggle_url(self):
        self.assertEqual(self.url, f'/follow_toggle/{self.followee.id}')
        
    def test_get_follow_toggle_redirect_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        
    def test_get_follow_toggle_for_followee(self):
        self.client.login(email=self.user.email, password='Password123')
        self.user.toggle_follow(self.followee)
        user_followers_before = self.user.follower_count()
        followee_followers_before = self.followee.follower_count()
        response = self.client.get(self.url, follow = True)
        user_followers_after = self.user.follower_count()
        followee_followers_after = self.followee.follower_count()
        self.assertEqual(user_followers_before, user_follower_count())
        self.assertEqual(followee_followers_before, followee_followers_after+1)
        response_url = reverse('friends_profile', kwargs={'email': self.followee.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'friends_profile.html')
        
    def test_get_follow_toggle_for_non_followee(self):
        self.client.login(email=self.user.email, password='Password123')
        user_followers_before = self.user.follower_count()
        followee_followers_before = self.followee.follower_count()
        response = self.client.get(self.url, follow = True)
        user_followers_after = self.user.follower_count()
        followee_followers_after = self.followee.follower_count()
        self.assertEqual(user_followers_before, user_follower_count())
        self.assertEqual(followee_followers_before+1, followee_followers_after)
        response_url = reverse('friends_profile', kwargs={'email': self.followee.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'friends_profile.html')
        
