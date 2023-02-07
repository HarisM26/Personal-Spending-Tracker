from django.test import TestCase
from expenditure.models import Limit
from django.core.exceptions import ValidationError


# Create your tests here.
class LimitModelTest(TestCase):
    def setUp(self):
        self.limit = Limit.objects.create(
            limit_amount=1000.00,
            spent_amount=0.00,
            start_date='2018-01-01',
            end_date='2018-01-08',
        )

    def test_limit_is_valid(self):
        try:
            self.limit.full_clean()
        except (ValidationError):
            self.fail('Limit is not valid')
    
    def test_correct_default_values(self):
        self.assertEqual(self.limit.status, 'not reached')
        self.assertEqual(self.limit.time_limit_type, 'weekly')

    def test_calculate_limit_approaching(self):
        self.limit.spent_amount = 900
        self.limit.save()
        self.assertEqual(self.limit.status, 'approaching')
    
    def test_calculate_limit_reached(self):
        self.limit.spent_amount = 1000
        self.limit.save()
        self.assertEqual(self.limit.status,'reached')



