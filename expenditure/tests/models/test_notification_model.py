from django.test import TestCase
from datetime import datetime
from django.core.exceptions import ValidationError
from expenditure.models import Notification

class NotificationModelTest(TestCase):

  def setUp(self):
    self.notification = Notification.objects.create(
    title = 'Approaching limit!',
    message = 'You are close to your set limit. Consider reducing your spending from now onwards',
    status = False,
    created = datetime.now()
    )

  def assert_notification_is_valid(self):
    try:
      self.notification.full_clean()
    except (ValidationError):
      self.fail('Notification should be valid')
  
  def assert_notification_is_invalid(self):
    with self.assertRaises(ValidationError):
      self.notification.full_clean()

  def test_notification(self):
    self.assert_notification_is_valid
    
