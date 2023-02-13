from django.test import TestCase
from datetime import datetime
from django.core.exceptions import ValidationError
from expenditure.models import Category,Limit,User
from decimal import *

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            user = User.objects.create(
                first_name = 'John',
                last_name = 'Doe',
                email = 'johndoe@email.com'
            ),
            name = "CategoryName",
            is_income = False
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

    def test_is_income_cannot_be_none(self):
        self.category.is_income = None
        self.assert_category_is_invalid()
        

    