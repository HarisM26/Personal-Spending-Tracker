from django.test import TestCase
from datetime import datetime, timedelta, date
from django.core.exceptions import ValidationError
from expenditure.models.categories import *
from expenditure.models.user import User
from decimal import *


class IncomeCategoryModelTest(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json']

    def setUp(self):
        self.category = IncomeCategory.objects.create(
            user=User.objects.get(email='johndoe@example.com'),
            name="CategoryName"
        )

    def assert_category_is_valid(self):
        try:
            self.category.full_clean()
        except:
            self.fail('Category should be valid')

    def assert_category_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_category(self):
        self.assert_category_is_valid()

    def test_name_cannot_be_blank(self):
        self.category.name = ""
        self.assert_category_is_invalid()

    def test_name_must_not_be_overlong(self):
        self.category.name = 'x' * 51
        self.assert_category_is_invalid()

    def test_name_is_correct_length(self):
        self.category.name = 'x' * 50
        self.assert_category_is_valid()
