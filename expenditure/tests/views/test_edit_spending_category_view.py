from datetime import date, timedelta, datetime
from django.test import TestCase
from django.urls import reverse
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import User
from expenditure.models.limit import Limit
from decimal import Decimal
from expenditure.forms import SpendingCategoryEditMultiForm
from expenditure.tests.helpers import reverse_with_next


class EditSpendingCategoryViewTestCase(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.com')
        self.category = SpendingCategory.objects.create(
            user=self.user,
            name='test_category',
            limit=Limit.objects.create(
                limit_amount=Decimal('10.00'),
                remaining_amount=Decimal('10.00'),
                time_limit_type='weekly',
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
        )
        self.url_list_spendings = reverse('spending')
        self.url_edit_category = reverse(
            'edit_spending_category', kwargs={'pk': self.category.id})

        self.edited_form = {
            'category-name': 'ChangedCategory',
            'limit-limit_amount': Decimal('500.00'),
            'limit-time_limit_type': 'monthly',
        }

    def test_edit_category_url(self):
        self.assertEqual(self.url_list_spendings, '/spending/')
        self.assertEqual(self.url_edit_category,
                         f"/spending-category/{self.category.id}/edit")

    def test_get_category(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url_edit_category)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_spending_category.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SpendingCategoryEditMultiForm))

    def test_get_category_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url_edit_category)
        response = self.client.get(self.url_edit_category)
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)

    def test_edit_category_changed(self):
        self.client.login(email=self.category.user.email,
                          password='Password123')
        response = self.client.post(
            self.url_edit_category, self.edited_form, follow=True)
        response_url = reverse('spending')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'spending.html')
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, self.edited_form['category-name'])
        self.assertEqual(self.category.limit.limit_amount,
                         self.edited_form['limit-limit_amount'])
        self.assertEqual(self.category.limit.time_limit_type,
                         self.edited_form['limit-time_limit_type'])

    def test_unsuccesful_category_edit(self):
        self.client.login(email=self.category.user.email,
                          password='Password123')
        self.edited_form['limit-limit_amount'] = Decimal('-500.00')
        response = self.client.post(
            self.url_edit_category, self.edited_form, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_spending_category.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SpendingCategoryEditMultiForm))
        self.category.refresh_from_db()
        self.assertEqual(Decimal('10.00'), self.category.limit.limit_amount)

    def test_post_category_edit_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url_edit_category)
        response = self.client.post(self.url_edit_category, self.edited_form)
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)
        self.assertEqual('test_category', self.category.name)
