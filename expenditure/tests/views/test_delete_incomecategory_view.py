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

        # 4 points
        self.transaction1 = {
            'title':'t1',
            'date':date.today(),
            'amount':Decimal('30.00'),
            'notes':'Some notes',
            'income_category':self.category.id,
        }

        # 4 points
        self.transaction2 = {
            'title':'t2',
            'date':date.today(),
            'amount':Decimal('50.00'),
            'notes':'Some',
            'income_category':self.category.id,
        }

        # 3 points
        self.transaction3 = {
            'title':'t3',
            'date':date.today(),
            'amount':Decimal('10.00'),
            'income_category':self.category.id,
        }
        
        # 4 points
        self.transaction4 = {
            'title':'t4',
            'date': date.today(),
            'amount': Decimal('45.00'),
            'notes':'notes',
            'income_category':self.category.id,
        }
        
        # 3 points
        self.transaction5 = {
            'title':'t5',
            'date':date.today(),
            'amount':Decimal('5.00'),
            'income_category':self.category.id,
        }

        # 18 points in total

        self.url_list_incomings = reverse('incomings')
        self.url_delete_category = reverse(
            'delete_income_category', kwargs={'pk': self.category.pk})
        self.url_add_income_transaction = reverse(
            'add_income_transaction', args=[self.category.pk])

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
        
    def test_points_deleted_with_category(self):
        self.client.login(email=self.category.user.email, password='Password123')

        #Add all transactions
        response = self.client.post(
            self.url_add_income_transaction, self.transaction1, follow=True)
        response = self.client.post(
            self.url_add_income_transaction, self.transaction2, follow=True)
        response = self.client.post(
            self.url_add_income_transaction, self.transaction3, follow=True)
        response = self.client.post(
            self.url_add_income_transaction, self.transaction4, follow=True)
        response = self.client.post(
            self.url_add_income_transaction, self.transaction5, follow=True)
        self.category.user.refresh_from_db()
        
        #User should have 18 points after adding these transactions
        self.assertEqual(self.category.user.points, 18)
        
        POINTS_BEFORE = self.category.user.points
        
        #Deleting category
        response = self.client.post(self.url_delete_category, follow = True)

        POINTS_AFTER = self.category.user.points

        #After deleting the points should be removed and the amount of points the user has is 0 now
        self.assertEqual(POINTS_BEFORE-POINTS_AFTER, 0)

        response_url = reverse('incomings')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)