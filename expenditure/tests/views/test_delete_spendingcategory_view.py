from datetime import date, timedelta, datetime
from django.test import TestCase
from django.urls import reverse
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import User
from expenditure.models.limit import Limit
from decimal import Decimal


class DeleteSpendingCategoryViewTestCase(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.category = SpendingCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name='test_category',
            limit=Limit.objects.create(
                limit_amount=Decimal('10.00'),
                remaining_amount=Decimal('10.00'),
                time_limit_type='weekly',
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )

        self.url_list_spending = reverse('spending')
        self.url_delete_category = reverse(
            'delete_spending_category', kwargs={'pk': self.category.pk})

    def test_delete_category_url(self):
        self.assertEqual(self.url_list_spending, '/spending/')
        self.assertEqual(self.url_delete_category,
                         f"/spending-category/{self.category.id}/delete")

    def test_category_deleted(self):
        self.client.login(email=self.category.user.email,
                          password='Password123')
        response = self.client.post(self.url_delete_category, follow=True)
        spending_category_exists = SpendingCategory.objects.filter(
            id=self.category.pk).exists()
        spending_category_limit_exists = Limit.objects.filter(
            id=self.category.limit.pk).exists()
        self.assertFalse(spending_category_exists)
        self.assertFalse(spending_category_limit_exists)
        response_url = reverse('spending')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
