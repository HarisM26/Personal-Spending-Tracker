from django.test import TestCase
from django.urls import reverse
from expenditure.models.user import User


class FeedViewTestCase(TestCase):
    """Tests of the feed view."""

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.com')
        self.url = reverse('feed')

    def test_feed_url(self):
        self.assertEqual(self.url, '/feed/')

    def test_get_feed(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
