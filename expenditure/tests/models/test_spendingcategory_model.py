from django.test import TestCase
from datetime import datetime, timedelta, date
from django.core.exceptions import ValidationError
from expenditure.models import SpendingCategory, Limit, User
from decimal import *

class SpendingCategoryModelTest(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json']

    def setUp(self):
        self.category = SpendingCategory.objects.create(
            user = User.objects.get(email='johndoe@example.com'),
            name = "CategoryName",
            limit = Limit.objects.create(
                limit_amount=Decimal('10.00'),
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=7)
            )
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

    
        

    