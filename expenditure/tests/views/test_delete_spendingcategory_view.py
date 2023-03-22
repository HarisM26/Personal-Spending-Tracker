from datetime import date, timedelta, datetime
from django.core.files.uploadedfile import SimpleUploadedFile
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

        self.image = SimpleUploadedFile(
            'receipt.jpg', b'blablabla', content_type='image/jpeg')
        
        # 4 points
        self.transaction1 = {
            'title':'t1',
            'date':date.today(),
            'amount':Decimal('30.00'),
            'notes':'Some notes',
            'spending_category':self.category.id,
            'is_current':True,
        }

        # 4 points
        self.transaction2 = {
            'title':'t2',
            'date':date.today(),
            'amount':Decimal('50.00'),
            'notes':'Some',
            'spending_category':self.category.id,
            'is_current':True,
        }

        # 3 points
        self.transaction3 = {
            'title':'t3',
            'date':date.today(),
            'amount':Decimal('10.00'),
            'spending_category':self.category.id,
            'is_current':True,
        }
        
        # 4 points
        self.transaction4 = {
            'title':'t4',
            'date': date.today(),
            'amount': Decimal('45.00'),
            'notes':'notes',
            'spending_category':self.category.id,
            'is_current':True,
        }
        
        # 3 points
        self.transaction5 = {
            'title':'t5',
            'date':date.today(),
            'amount':Decimal('5.00'),
            'spending_category':self.category.id,
            'is_current':True,
        }

        # 18 points in total

        self.url_list_spending = reverse('spending')
        self.url_delete_category = reverse(
            'delete_spending_category', kwargs={'pk': self.category.pk})
        self.url_add_transaction = reverse(
            'add_spending_transaction', args=[self.category.id])

    def test_delete_category_url(self):
        self.assertEqual(self.url_list_spending, '/spending/')
        self.assertEqual(self.url_delete_category,
                         f"/spending-category/{self.category.id}/delete")

    def test_category_deleted(self):
        self.client.login(email=self.category.user.email, password='Password123')
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
        
    def test_points_deleted_with_category(self):
        self.client.login(email=self.category.user.email, password='Password123')

        #Add all transactions
        response = self.client.post(
            self.url_add_transaction, self.transaction1, follow=True)
        response = self.client.post(
            self.url_add_transaction, self.transaction2, follow=True)
        response = self.client.post(
            self.url_add_transaction, self.transaction3, follow=True)
        response = self.client.post(
            self.url_add_transaction, self.transaction4, follow=True)
        response = self.client.post(
            self.url_add_transaction, self.transaction5, follow=True)
        self.category.user.refresh_from_db()
        
        #User should have 18 points after adding these transactions
        self.assertEqual(self.category.user.points, 18)
        
        POINTS_BEFORE = self.category.user.points
        
        #Deleting category
        response = self.client.post(self.url_delete_category, follow = True)

        POINTS_AFTER = self.category.user.points

        #After deleting the points should be removed and the amount of points the user has is 0 now
        self.assertEqual(POINTS_BEFORE-POINTS_AFTER, 0)

        response_url = reverse('spending')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)