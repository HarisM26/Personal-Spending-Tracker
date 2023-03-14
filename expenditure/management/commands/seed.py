from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from expenditure.models import User


from faker import Faker


class Command(BaseCommand):

    help = 'Seeds database with fake data'

    USER_COUNT = 250
    DEFAULT_PASSWORD = 'SeededUserPassword123'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.seed_users()
        self.users = User.objects.all()
        self.stdout.write(self.style.SUCCESS('Users seeded'))

    def seed_users(self):
        self.stdout.write(self.style.SUCCESS('Seeding users...'))
        new_seeded_users = 0
        while new_seeded_users < self.USER_COUNT:
            try:
                self.create_user()
                new_seeded_users += 1
                self.stdout.write(self.style.SUCCESS(
                    f'User {new_seeded_users} seeded'))
            except IntegrityError:
                continue

    def create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = generate_email(first_name, last_name)
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=self.DEFAULT_PASSWORD,
            is_active=True,
            is_staff=False,
        )
        user.set_password(self.DEFAULT_PASSWORD)


def generate_email(first_name, last_name):
    return '{}.{}@from.seed'.format(first_name.lower(), last_name.lower())
