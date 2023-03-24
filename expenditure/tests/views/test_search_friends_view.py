from django.test import TestCase
from django.urls import reverse
from expenditure.models.user import User
from expenditure.forms import UpdateUserForm
from expenditure.tests.helpers import reverse_with_next
from django.contrib import messages


class SearchFriendsTest(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.com')
        self.url = reverse('search_friends')
        self.form_input = {
            'first_name': 'John2',
        }
        self.url_privacy = reverse('toggle_privacy')

    def test_profile_url(self):
        self.assertEqual(self.url, '/search_friends/')

    def test_search_friends_accessible(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('search_friends.html', (t.name for t in response.templates))

    def test_search_friends(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)


    def test_get_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)
    
    def test_privacy_toggle_url(self):
        self.assertEqual(self.url_privacy, '/settings/toggle_privacy')

    def test_get_privacy_toggle_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url_privacy)
        response = self.client.get(self.url_privacy)
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)
    
    def test_toggle_privacy(self):
        self.client.login(privacy='johndoe@example.com', password='Password123')
        previous = self.user.toggle_privacy
        response = self.client.get(self.url_privacy)
        now = User.objects.get(email='johndoe@example.com').toggle_privacy
        self.assertEqual(previous, now)
        response_url = reverse('settings')
    
    def test_toggle_privacy_off(self):
        self.user.toggle_privacy = 'ON'
        self.user.save()
        self.client.login(privacy='johndoe@example.com', password='Password123')
        previous = self.user.toggle_privacy
        response = self.client.get(self.url_privacy)
        now = User.objects.get(email='johndoe@example.com').toggle_privacy
        self.assertEqual(previous, now)
        response_url = reverse('settings')
