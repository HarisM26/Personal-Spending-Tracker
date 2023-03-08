from datetime import date,timedelta,datetime
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from betterforms.multiform import MultiModelForm
from expenditure.models import Transaction, SpendingCategory, Limit, User
from expenditure.forms import SpendingCategoryEditMultiForm
from decimal import Decimal

class EditSpendingCategoryViewTestCase(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
              'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.category = SpendingCategory.objects.create(
            user = User.objects.get(email='johndoe@example.com'),
            name = 'test_category',
            limit = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                remaining_amount = Decimal('10.00'),
                time_limit_type = 'weekly',
                start_date= date.today(),
                end_date= datetime.now() + timedelta(days=7)
            )
        )
        self.url_list_spendings = reverse('spending')
        self.url_edit_category = reverse('edit_spending_category', kwargs={'pk': self.category.id})

        self.category2 = SpendingCategory.objects.create(
            user = User.objects.get(email='johndoe@example.com'),
            name = 'ChangedCategory',
            limit = Limit.objects.create(
                limit_amount=Decimal('500.00'),
                remaining_amount = Decimal('500.00'),
                time_limit_type = 'monthly',
                start_date= date.today(),
                end_date= datetime.now() + timedelta(days=7)
            )
        )

        self.edited_form = {
            'category-name': self.category.name,
            'limit-limit_amount': self.category.limit.limit_amount,
            'limit-time_limit_type': self.category.limit.time_limit_type
        }

    def test_edit_category_url(self):
        self.assertEqual(self.url_list_spendings,'/spending/')
        self.assertEqual(self.url_edit_category, f"/spending-category/{self.category.id}/edit")

    def test_edit_category_changed(self):
        self.client.login(email=self.category.user.email, password='Password123')
        response = self.client.post(self.url_edit_category, self.edited_form, follow=True)
        self.assertEqual(self.category.name, self.edited_form['category-name'])
        self.assertEqual(self.category.limit.limit_amount, self.edited_form['limit-limit_amount'])
        self.assertEqual(self.category.limit.time_limit_type, self.edited_form['limit-time_limit_type'])
        response_url = reverse('spending')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200 )



