from django.test import TestCase
from expenditure.models import Limit
from django.core.exceptions import ValidationError
from datetime import timedelta,datetime
from decimal import Decimal



# Create your tests here.
class LimitModelTest(TestCase):
    def setUp(self):
        self.limit = Limit.objects.create(
            limit_amount=1000.00,
            start_date=datetime.date(datetime.now()),
            end_date=datetime.date(datetime.now()) + timedelta(days=7),
        )

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

    def test_limit_amount_cannot_be_negative(self):
        self.limit.limit_amount = Decimal('-1000.00')
        self.assert_limit_is_invalid()
    
    def test_limit_amount_cannot_be_zero(self):
        self.limit.limit_amount = Decimal('0.00')
        self.assert_limit_is_invalid()
    
    def test_limit_amount_cannot_have_more_than_2_decimal_places(self):
        self.limit.limit_amount = Decimal('1000.001')
        self.assert_limit_is_invalid()
    
    def test_limit_amount_can_have_10_digits(self):
        self.limit.limit_amount = Decimal('12345678.91')
        self.assert_limit_is_valid()

    def test_limit_amount_cannot_have_more_than_10_digits(self):
        self.limit.limit_amount = Decimal('123456789.00')
        self.assert_limit_is_invalid()
    
    def test_limit_amount_cannot_be_null(self):
        self.limit.limit_amount = None
        self.assert_limit_is_invalid()

    def test_remaining_amount_cannot_have_more_than_2_decimal_places(self):
        self.limit.remaining_amount = Decimal('1000.001')
        self.assert_limit_is_invalid()
    
    def test_remaining_amount_can_have_10_digits(self):
        self.limit.remaining_amount = Decimal('12345678.91')
        self.assert_limit_is_valid()
    
    def test_remaining_amount_cannot_have_more_than_10_digits(self):
        self.limit.remaining_amount = Decimal('123456789.00')
        self.assert_limit_is_invalid()
    
    def test_remaining_amount_is_zero_by_default(self):
        self.assertEqual(self.limit.remaining_amount, Decimal('0.00'))
    
    def test_status_is_not_reached_by_default(self):
        self.assertEqual(self.limit.status, 'not reached')

    #TODO: add tests for start_date and end_date (end_date cannot be before start_date)
    
    #def test_correct_default_values(self):
    #    self.assertEqual(self.limit.status, 'not reached')
    #    self.assertEqual(self.limit.time_limit_type, 'weekly')

    #def test_calculate_limit_approaching(self):
    #    self.limit.spent_amount = 900
    #    self.limit.save()
    #    self.assertEqual(self.limit.status, 'approaching')
    #
    #def test_calculate_limit_reached(self):
    #    self.limit.spent_amount = 1000
    #    self.limit.save()
    #    self.assertEqual(self.limit.status,'reached')
    #
    #def test_calculate_limit_not_reached(self):
    #    self.limit.spent_amount = 899
    #    self.limit.save()
    #    self.assertEqual(self.limit.status, 'not reached')


