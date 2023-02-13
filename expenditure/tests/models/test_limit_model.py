from django.test import TestCase
from datetime import timedelta,datetime
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
        except (ValidationError):
            self.fail('Limit is not valid')
    
    def assert_limit_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.limit.full_clean()
    
    def test_limit_is_valid(self):
        self.assert_limit_is_valid()

    def test_spent_amount_cannot_be_blank(self):
        self.limit.spent_amount = ''
        self.assert_limit_is_invalid()

    def test_limit_amount_cannot_be_negative(self):
        self.limit.limit_amount = -1000.00
        self.assert_limit_is_invalid()

    def test_limit_amount_cannot_be_zero(self):
        self.limit.limit_amount = 0.00
        self.assert_limit_is_invalid()
    
    def test_limit_amount_cannot_have_more_than_2_decimal_places(self):
        self.limit.limit_amount = 1000.001
        self.assert_limit_is_invalid()
    
    def test_limit_amount_can_have_10_digits(self):
        self.limit.limit_amount = 12345678.91
        self.assert_limit_is_valid()

    def test_limit_amount_cannot_have_more_than_10_digits(self):
        self.limit.limit_amount = 123456789.00
        self.assert_limit_is_invalid()
    
    def test_limit_amount_cannot_be_null(self):
        self.limit.limit_amount = None
        self.assert_limit_is_invalid()

    def test_remaining_amount_cannot_have_more_than_2_decimal_places(self):
        self.limit.remaining_amount = 1000.001
        self.assert_limit_is_invalid()
    
    def test_remaining_amount_can_have_10_digits(self):
        self.limit.remaining_amount = 12345678.91
        self.assert_limit_is_valid()
    
    def test_remaining_amount_cannot_have_more_than_10_digits(self):
        self.limit.remaining_amount = 123456789.00
        self.assert_limit_is_invalid()
    
    def test_remaining_amount_is_zero_by_default(self):
        self.assertEqual(self.limit.remaining_amount, 0.00)
    
    def test_status_is_not_reached_by_default(self):
        self.assertEqual(self.limit.status, 'not reached')

    # def test_correct_default_values(self):
    #    self.assertEqual(self.limit.status, 'not reached')
    #    self.assertEqual(self.limit.time_limit_type, 'weekly')

    # def test_calculate_limit_approaching(self):
    #    self.limit.spent_amount = 900
    #    self.limit.save()
    #    self.assertEqual(self.limit.status, 'approaching')
    
    # def test_calculate_limit_reached(self):
    #    self.limit.spent_amount = 1000
    #    self.limit.save()
    #    self.assertEqual(self.limit.status,'reached')
    
    # def test_calculate_limit_not_reached(self):
    #    self.limit.spent_amount = 899
    #    self.limit.save()
    #    self.assertEqual(self.limit.status, 'not reached')

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

    """k"""
    
    

    
    
    
    
    

    #TODO: add tests for start_date and end_date (end_date cannot be before start_date)
    
    



    