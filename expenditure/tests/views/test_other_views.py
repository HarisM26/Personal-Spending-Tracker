from django.test import TestCase
from django.urls import reverse
from expenditure.models.user import User


class NewsPageViewTest(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('news_page')
        self.user = User.objects.get(email='johndoe@example.com')

    def test_news_page_url(self):
        self.assertEqual(self.url, '/news_page/')

    def test_get_news_pages(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_page.html')

    def test_news_page_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('feed')
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')


class ContactViewTest(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('contact')

    def test_contact_url(self):
        self.assertEqual(self.url, '/contact/')
