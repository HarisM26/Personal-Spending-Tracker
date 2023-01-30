from django.test import TestCase
from datetime import datetime
from django.core.exceptions import ValidationError
from expenditure.models import Notification

class NotificationModelTest(TestCase):

  def setUp(self):
    self.notification = Notification.objects.create(
    title = 'Approaching limit!',
    message = 'You are close to your set limit. Consider reducing your spending from now onwards',
    status = 'unread',
    time_created = datetime.time(datetime.now()),
    date_created = datetime.date(datetime.now())
    )
  
  def create_other_notification(self):
    notification = Notification.objects.create(
    title = 'Approaching limit!',
    message = 'You are close to your set limit. Consider reducing your spending from now onwards',
    status = 'unread',
    time_created = datetime.time(datetime.now()),
    date_created = datetime.date(datetime.now())
    )
    return notification

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

  """test title field"""
  def test_title_cannot_be_blank(self): 
    self.notification.title = ''
    self.assert_notification_is_invalid()

  def test_title_may_exist(self):
    other_notification = self.create_other_notification()
    self.notification.title = other_notification.title
    self.assert_notification_is_valid()

  def test_title_should_have_up_to_300_characters(self):
    self.notification.title = 'x' * 299
    self.assert_notification_is_valid() 

  def test_title_cannot_have_more_than_300_characters(self):
    self.notification.title = 'x' * 301
    self.assert_notification_is_invalid()

  """test message field"""
  def test_message_cannot_be_blank(self): 
    self.notification.message = ''
    self.assert_notification_is_invalid()

  def test_message_may_exist(self):
    other_notification = self.create_other_notification()
    self.notification.message = other_notification.message
    self.assert_notification_is_valid()

  def test_message_should_have_up_to_1200_characters(self):
    self.notification.message = 'x' * 1199
    self.assert_notification_is_valid() 

  def test_message_cannot_have_more_than_1200_characters(self):
    self.notification.message = 'x' * 1201
    self.assert_notification_is_invalid()   

  """test status field"""
  def test_notification_status_cannot_be_empty(self):
    self.notification.status = ''
    self.assert_notification_is_invalid()

  """test time field"""
  def test_notification_time_cannot_have_minutes_greater_than_59(self):
    self.notification.time_created = '09:60'
    self.assert_notification_is_invalid()

  def test_notification_time_cannot_have_hours_greater_than_23(self):
    self.notification.time_created = '24:00'
    self.assert_notification_is_invalid()

  """test date field"""
  def test_notification_date_must_have_a_day(self):
    self.notification.date_created = '2022-11'
    self.assert_notification_is_invalid()
    
  def test_notification_date_must_have_day_between_1_and_31(self):
    self.notification.date_created = '2022-11-32'
    self.assert_notification_is_invalid()
    
  def test_notification_date_cannot_have_0_day(self):
    self.notification.date_created = '2022-11-00'
    self.assert_notification_is_invalid()
    
  def test_notification_date_must_have_a_month(self):
    self.notification.date_created = '2022-23'
    self.assert_notification_is_invalid()

  def test_notification_date_cannot_have_0_month(self):
    self.notification.date_created = '2022-00-23'
    self.assert_notification_is_invalid()
    
  def test_notification_date_must_have_month_between_1_and_12(self):
    self.notification.date_created = '2022-13-23'
    self.assert_notification_is_invalid()   

  def test_notification_date_must_have_a_year(self):
    self.notification.date_created = '11-23'
    self.assert_notification_is_invalid()

