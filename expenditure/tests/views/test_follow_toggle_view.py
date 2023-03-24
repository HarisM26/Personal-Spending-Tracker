from django.test import TestCase
from django.urls import reverse
from expenditure.models.user import User
from expenditure.tests.helpers import reverse_with_next


class ShowUserTest(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.com')
        self.followee = User.objects.get(email='janedoe@example.com')
        self.url = reverse('follow_toggle', kwargs={'id': self.followee.id})

    # def test_follow_toggle_url(self):
    #     self.assertEqual(
    #         self.url, f'/search_friends/follow_toggle/{self.followee.id}')

    # def test_get_follow_toggle_redirect_when_not_logged_in(self):
    #     redirect_url = reverse_with_next('log_in', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url,
    #                          status_code=302, target_status_code=200)

    # def test_get_follow_toggle_for_followee(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     self.user.toggle_follow(self.followee.id)
    #     user_followers_before = self.user.follower_count()
    #     followee_followers_before = self.followee.follower_count()
    #     response = self.client.get(self.url, follow=True)
    #     user_followers_after = self.user.follower_count()
    #     followee_followers_after = self.followee.follower_count()
    #     self.assertEqual(user_followers_before, user_followers_after)
    #     self.assertEqual(followee_followers_before, followee_followers_after+1)
    #     response_url = reverse('search_friends')
    #     self.assertRedirects(response, response_url,
    #                          status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'search_friends.html')

    # def test_get_follow_toggle_for_non_followee(self):
    #     self.client.login(email=self.user.email, password='Password123')
    #     user_followers_before = self.user.follower_count()
    #     followee_followers_before = self.followee.follower_count()
    #     response = self.client.get(self.url, follow=True)
    #     user_followers_after = self.user.follower_count()
    #     followee_followers_after = self.followee.follower_count()
    #     self.assertEqual(user_followers_before, user_followers_after)
    #     self.assertEqual(followee_followers_before+1, followee_followers_after)
    #     response_url = reverse('search_friends')
    #     self.assertRedirects(response, response_url,
    #                          status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'search_friends.html')
    
