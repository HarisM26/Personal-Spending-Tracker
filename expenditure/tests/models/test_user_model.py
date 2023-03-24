'''Unit test for the User Model'''
from django.core.exceptions import ValidationError
from django.test import TestCase
from expenditure.models.user import User


class UserModelTestCase(TestCase):

    fixtures = ['expenditure/tests/fixtures/default_user.json',
                'expenditure/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.com')

    # tests for user validity
    def test_valid_user(self):
        self._assert_user_is_valid()

    # tests for the first name
    def test_first_name_cannot_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_can_already_exist(self):
        second_user = second_user = User.objects.get(
            email='janedoe@example.com')
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_cannot_be_over_30_characters(self):
        self.user.first_name = 'x' * 30
        self._assert_user_is_invalid()

    def test_first_name_can_be_up_to_30_characters(self):
        self.user.first_name = 'x' * 30
        self._assert_user_is_valid()

    def test_first_name_cannot_be_over_30_characters(self):
        self.user.first_name = 'x' * 31
        self._assert_user_is_invalid()

    # tests for the last name
    def test_last_name_cannot_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_can_already_exist(self):
        second_user = User.objects.get(email='janedoe@example.com')
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_can_be_up_to_150_characters(self):
        self.user.last_name = 'x' * 150
        self._assert_user_is_valid()

    def test_last_name_cannot_be_over_150_characters(self):
        self.user.last_name = 'x' * 151
        self._assert_user_is_invalid()

    # tests for the email
    def test_email_cannot_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = second_user = User.objects.get(
            email='janedoe@example.com')
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_cannot_be_over_255_characters(self):
        self.user.email = 'x' * 256
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_multiple_at_symbols(self):
        self.user.email = 'willsmith@@example.org'
        self._assert_user_is_invalid()

    def test_toggle_follow_user(self):
        jane = User.objects.get(email='janedoe@example.com')
        self.assertFalse(self.user.is_following(jane))
        self.assertFalse(jane.is_following(self.user))
        self.user.toggle_follow(jane)
        self.assertTrue(self.user.is_following(jane))
        self.assertFalse(jane.is_following(self.user))
        self.user.toggle_follow(jane)
        self.assertFalse(self.user.is_following(jane))
        self.assertFalse(jane.is_following(self.user))

    def test_follow_counters(self):
        jane = User.objects.get(email='janedoe@example.com')
        willow = User.objects.get(email='willowsmith@example.org')
        sarah = User.objects.get(email='sarahkipling@example.org')
        self.user.toggle_follow(jane)
        self.user.toggle_follow(willow)
        self.user.toggle_follow(sarah)
        jane.toggle_follow(willow)
        jane.toggle_follow(sarah)
        self.assertEqual(self.user.follower_count(), 0)
        self.assertEqual(self.user.followee_count(), 3)
        self.assertEqual(jane.follower_count(), 1)
        self.assertEqual(jane.followee_count(), 2)
        self.assertEqual(willow.follower_count(), 2)
        self.assertEqual(willow.followee_count(), 0)
        self.assertEqual(sarah.follower_count(), 2)
        self.assertEqual(sarah.followee_count(), 0)

    def test_toggle_notification(self):
        self.assertTrue(self.user.toggle_notification, 'ON')
        self.user.toggle_notification = 'OFF'
        self.assertTrue(self.user.toggle_notification, 'OFF')

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def test_successful_create_superuser(self):
            super_user = User.objects.create_superuser(
                    email = 'superuser@mail.ru',
                    first_name = 'John',
                    last_name = 'Doe',
                    password = 'Password123',
                )
            self.assertTrue(super_user.is_superuser)

    def test_unsuccessful_create_superuser_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email = '',
                first_name = 'John',
                last_name = 'Doe',
                password = 'Password123',
            )

    def test_unsuccessful_create_superuser_without_rights(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email = 'director2@mail.ru',
                first_name = 'John',
                last_name = 'Doe',
                password = 'Password123',
                is_superuser = False,
            )
    
    def test_unsuccessful_create_superuser_without_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email = 'director2@mail.ru',
                first_name = 'John',
                last_name = 'Doe',
                password = 'Password123',
                is_staff = False,
            )
    
    def test_full_name(self):
        full_name = f'{self.user.first_name} {self.user.last_name}'
        self.assertEqual(self.user.full_name(), full_name)

    def test_str(self):
        self.assertEqual(str(self.user), f'{self.user.email}')
    
    

