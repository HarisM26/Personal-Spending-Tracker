from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from expenditure.models import User
from random import randint, random, sample


from faker import Faker


class Command(BaseCommand):

    help = 'Seeds database with fake data'

    USER_COUNT = 50
    HIGH_POINT_USER_BIAS = 0.1  # Probability of a high point seeded user being generated
    HIGH_POINT_USER_MIN = 5000
    HIGH_POINT_USER_MAX = 25000
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
                self.create_user(new_seeded_users)
                new_seeded_users += 1
                self.stdout.write(self.style.SUCCESS(
                    f'User {new_seeded_users} seeded'))
            except IntegrityError:
                continue

    def create_user(self, new_seeded_users):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = generate_email(first_name, last_name)
        points = self.get_points()
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=self.DEFAULT_PASSWORD,
            points=points,
            is_active=True,
            is_staff=False,
        )
        user.set_password(self.DEFAULT_PASSWORD)
        self.add_followings(user, new_seeded_users)

    def add_followings(self, user, new_seeded_users):
        self.stdout.write(self.style.SUCCESS('Adding followings...'))
        num_following = randint(0, new_seeded_users)
        all_users = list(User.objects.all())
        random_users = sample(all_users, num_following)
        for random_user in random_users:
            user.toggle_follow(random_user)

    def get_points(self):
        res = random()
        if res < self.HIGH_POINT_USER_BIAS:
            return randint(self.HIGH_POINT_USER_MIN, self.HIGH_POINT_USER_MAX)
        return randint(0, self.HIGH_POINT_USER_MIN)


def generate_email(first_name, last_name):
    return '{}.{}@from.seed'.format(first_name.lower(), last_name.lower())
