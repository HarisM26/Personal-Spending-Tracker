from django.test import TestCase
from datetime import datetime
from django.core.exceptions import ValidationError
from expenditure.models import Category,Limit,User
from decimal import *

class LimitModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            user = User.objects.create(
                first_name = 'John',
                last_name = 'Doe',
                email = 'johndoe@email.com'
            ),
            name = "CategoryName",
        )
        self.limit = Limit.objects.create(category=self.category, limit_amount=Decimal('1000.00'), spent_amount=Decimal('0.00'))
        

    def assert_limit_is_valid(self):
        try:
            self.limit.full_clean()
        except:
            self.fail('Limit should be valid')
    
    def assert_limit_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.limit.full_clean()
    
    def test_limit(self):
        self.assert_limit_is_valid()


    def test_spent_amount_cannot_be_blank(self):
        self.limit.spent_amount = ''
        self.assert_limit_is_invalid()

    def test_spent_amount_cannot_be_negative(self):
        self.limit.spent_amount = -1
        self.assert_limit_is_invalid()

    def test_setLimitAmount_assigns_valid_limit(self):
        self.limit.setLimitAmount(-1)
        if (self.limit.getLimitAmount() >= 0):
            self.assert_limit_is_valid()
        else:
            self.assert_limit_is_invalid()

    def test_setSpentAmount_assigns_valid_spent_amount_in_limit(self):
        self.limit.setSpentAmount(-1)
        if (self.limit.getSpentAmount() >= 0):
            self.assert_limit_is_valid()
        else:
            self.assert_limit_is_invalid()

    def test_addSpentAmount_rejects_negative_numbers(self):
        # addSpentAmount will return -1 if the number is negative
        # otherwise, it updates spent_amount in limit
        if(self.limit.addSpentAmount(-1) == -1):
            self.assert_limit_is_valid()

    def test_addSpentAmount_correctly_adds_to_spent_amount(self):
        self.limit.addSpentAmount(100)
        if(self.limit.getSpentAmount() == 200):
            self.assert_limit_is_valid()
        else:
            self.assert_limit_is_invalid()

    def test_subtractSpentAmount_correctly_subtracts_from_spent_amount(self):
        self.limit.subtractSpentAmount(100)
        if(self.limit.getSpentAmount() == 0):
            self.assert_limit_is_valid()
        else:
            self.assert_limit_is_invalid()
    