from django.test import TestCase
from django.urls import reverse
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import User


class DeleteIncomeCategoryViewTestCase(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.category = IncomeCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name='test_category',
        )

        self.url_list_incomings = reverse('incomings')
        self.url_delete_category = reverse(
            'delete_income_category', kwargs={'pk': self.category.pk})

    def test_delete_category_url(self):
        self.assertEqual(self.url_list_incomings, '/incomings/')
        self.assertEqual(self.url_delete_category,
                         f"/income-category/{self.category.id}/delete")

    def test_category_deleted(self):
        self.client.login(email=self.category.user.email,
                          password='Password123')
        response = self.client.post(self.url_delete_category, follow=True)
        income_category_exists = IncomeCategory.objects.filter(
            id=self.category.pk).exists()
        self.assertFalse(income_category_exists)
        response_url = reverse('incomings')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
