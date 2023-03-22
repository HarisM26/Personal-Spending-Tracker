from django.test import TestCase
from django.urls import reverse
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import User


class EditIncomeCategoryViewTestCase(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.category = IncomeCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name='test_category',
        )

        self.url_list_incomings = reverse('incomings')
        self.url_edit_category = reverse(
            'edit_income_category', kwargs={'pk': self.category.id})

        self.edited_form = {
            'name': 'ChangedIncomeCategory'
        }

    def test_edit_category_url(self):
        self.assertEqual(self.url_list_incomings, '/incomings/')
        self.assertEqual(self.url_edit_category,
                         f"/income-category/{self.category.id}/edit")

    def test_edit_category_changed(self):
        self.client.login(email=self.category.user.email,
                          password='Password123')
        response = self.client.post(
            self.url_edit_category, self.edited_form, follow=True)
        income_category = IncomeCategory.objects.get(id=self.category.pk)
        self.assertEqual(income_category.name, self.edited_form['name'])
        response_url = reverse('incomings')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
