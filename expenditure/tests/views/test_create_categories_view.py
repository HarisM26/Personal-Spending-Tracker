from datetime import date, timedelta, datetime
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import User
from expenditure.models.limit import Limit
from decimal import Decimal
from expenditure.forms import CategoryCreationMultiForm


class CreateCategoryViews(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.category = SpendingCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name='test_category',
            limit=Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )
        self.user = User.objects.get(email='johndoe@example.com')

        self.category_2 = IncomeCategory.objects.create(
            user=User.objects.get(email='janedoe@example.com'),
            name='test2_category',
        )

        self.spending_form = {
            'category-name': 'shopping',
            'limit-limit_amount': Decimal('400'),
            'limit-time_limit_type': 'weekly',
        }

        self.incoming_form = {
            'name': 'salary',
        }

        self.url_list_spendings = reverse('spending')
        self.url_add_category = reverse('create_category')
        self.url_add_income_category = reverse('create_incoming_category')

    def test_catgeory_urls(self):
        self.assertEqual(self.url_list_spendings, '/spending/')
        self.assertEqual(self.url_add_category, f'/create_category/')
        self.assertEqual(self.url_add_income_category, f'/create_incoming_category/')

    def test_catgeory_urls_are_accessible(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response_list_spendings = self.client.get(self.url_list_spendings)
        response_add_category = self.client.get(self.url_add_category)
        response_add_income_category = self.client.get(self.url_add_income_category)

        self.assertEqual(response_list_spendings.status_code, 200)
        self.assertEqual(response_add_category.status_code, 200)
        self.assertEqual(response_add_income_category.status_code, 200)

        self.assertIn('spending.html', (t.name for t in response_list_spendings.templates))
        self.assertIn('create_category.html', (t.name for t in response_add_category.templates))
        self.assertIn('create_incoming_category.html', (t.name for t in response_add_income_category.templates))

    def test_add_category(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(self.url_add_category)
        form = response.context['form']
        self.assertTrue(isinstance(form, CategoryCreationMultiForm))
        self.assertTrue(form.is_valid)
        self.assertFalse(form.is_bound)
        before_count = SpendingCategory.objects.all().count()
        response = self.client.post(self.url_add_category, self.spending_form, follow=True)
        after_count = SpendingCategory.objects.count()
        self.assertEqual(after_count, before_count+1)
        category = SpendingCategory.objects.get(name='shopping')
        self.assertEqual(self.user, category.user)
        self.assertEqual(response.status_code, 200)
    
    def test_unsuccessfully_add_category(self):
        input_form = {
            'category-name': 'shopping',
            'limit-limit_amount': Decimal('400'),
            'limit-time_limit_type': 'week',
        }
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(self.url_add_category)
        form = response.context['form']
        self.assertTrue(isinstance(form, CategoryCreationMultiForm))
        self.assertTrue(form.is_valid)
        self.assertFalse(form.is_bound)
        before_count = SpendingCategory.objects.all().count()
        response = self.client.post(self.url_add_category, input_form, follow=True)
        after_count = SpendingCategory.objects.count()
        self.assertEqual(after_count, before_count)


    def test_income_add_category(self):
        self.client.login(email='johndoe@example.com', password='Password123')
        response = self.client.get(self.url_add_income_category)
        before_count = IncomeCategory.objects.all().count()
        response = self.client.post(self.url_add_income_category, self.incoming_form, follow=True)
        after_count = IncomeCategory.objects.count()
        self.assertEqual(after_count, before_count+1)
        category = IncomeCategory.objects.get(name='salary')
        self.assertEqual(self.user, category.user)
        self.assertEqual(response.status_code, 200)
    
    

