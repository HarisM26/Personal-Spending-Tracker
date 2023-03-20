from django.test import TestCase
from expenditure.forms import *
from expenditure.models.categories import *
from expenditure.models.user import User


class IncomeCategoryFormTest(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.category = IncomeCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name='test_category'
        )

        self.form_input = {
            'name': 'Test_Category'
        }

    def test_form_contains_required_fields(self):
        form = IncomeCategoryForm()
        self.assertIn('name', form.fields)

    def test_form_accepts_valid_input(self):
        form = IncomeCategoryForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_name(self):
        self.form_input['name'] = ''
        form = IncomeCategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_rejects_overlong_name(self):
        self.form_input['name'] = 'x' * 51
        form = IncomeCategoryForm(data=self.form_input)
        self.assertFalse(form.is_valid())
