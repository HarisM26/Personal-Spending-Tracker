from django.test import TestCase
from django.urls import reverse
from expenditure.models.user import User
from decimal import Decimal
from expenditure.helpers import check_league


class LeaderboardViewTest(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.com')
        self.user.points = 23
        self.user.save()

        self.user_1 = User.objects.get(email='janedoe@example.com')
        self.user_1.points = 45
        self.user_1.save()

        self.user_2 = User.objects.get(email='willowsmith@example.org')
        self.user_2.league_status = 'silver'
        self.user_2.points = 290
        self.user_2.save()

        self.user_3 = User.objects.get(email='sarahkipling@example.org')
        self.user_3.league_status = 'silver'
        self.user_3.points = 290
        self.user_3.save()

        self.url = reverse('leaderboard')

    def test_leaderboard_url(self):
        self.assertEqual(self.url, '/leaderboard/')

    def test_leaderboard_url_are_accessible(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertIn('leaderboard.html', (t.name for t in response.templates))

    def test_user_league_order(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(self.url)
        user_place = response.context['user_place']
        user_overall_place = response.context['user_overall_place']

        self.assertEqual(2, user_place)
        self.assertEqual(4, user_overall_place)
    
    def test_bronze_status_update(self):
        self.user.points = 200
        self.user.save()
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(self.url)
        user_league_status = User.objects.get(email='johndoe@example.com').league_status
        self.assertEqual('silver', user_league_status)
    
    def test_silver_status_update(self):
        self.user_1.league_status = 'silver'
        self.user_1.points = 600
        self.user_1.save()
        self.client.login(email='janedoe@example.com', password='Password123')
        response = self.client.get(self.url)
        user_league_status = User.objects.get(email='janedoe@example.com').league_status
        self.assertEqual('gold', user_league_status)
    
    def test_gold_status_update(self):
        self.user_2.league_status = 'gold'
        self.user_2.points = 1800
        self.user_2.save()
        self.client.login(email='willowsmith@example.org', password='Password123')
        response = self.client.get(self.url)
        user_league_status = User.objects.get(email='willowsmith@example.org').league_status
        self.assertEqual('platinum', user_league_status)

    def test_diamond_status_update(self):
        self.user_3.league_status = 'platinum'
        self.user_3.points = 5000
        self.user_3.save()
        self.client.login(email='sarahkipling@example.org', password='Password123')
        response = self.client.get(self.url)
        user_league_status = User.objects.get(email='sarahkipling@example.org').league_status
        self.assertEqual('diamond', user_league_status)
    
