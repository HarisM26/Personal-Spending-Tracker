from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from expenditure.models.user import User
from expenditure.models.categories import SpendingCategory
from expenditure.models.limit import Limit
from expenditure.models.transactions import SpendingTransaction
from expenditure.views.category_views import create_default_categories
from expenditure.helpers import request_less_check_league
from random import random, randint, choice, sample
from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404

from decimal import Decimal
from faker import Faker
from faker.providers import DynamicProvider


class Command(BaseCommand):

    """
    Comment out init() check when seeding
    TODO: Make seeder work without need to comment out in this wasy
    """

    help = 'Seeds database with fake data'

    USERS_PER_LEAGUE = 20
    MAX_TRANSACTIONS_PER_CATEGORY_PER_MONTH = 5

    # Number of months prior to current date when transactions can be made
    MAX_START_OF_TRANSACTIONS_FOR_USER = 14

    DEFAULT_PASSWORD = 'SeededUserPassword123'
    LEAGUE_BOUNDS = [(0, 200), (200, 600), (600, 1800),
                     (1800, 5000), (5000, 7000)]

    def __init__(self):
        super().__init__()
        category_name_provider = DynamicProvider(
            provider_name="category_name",
            elements=["Private", "Self-improvement", "Health",
                      "Clothing", "Online shopping", "Other"]
        )
        transaction_title_provider = DynamicProvider(
            provider_name="transaction_title",
            elements=["Food", "Night out", "Friends",
                      "Travel", "Online shopping", "Other"]
        )
        self.faker = Faker('en_GB')
        self.faker.add_provider(category_name_provider)
        self.faker.add_provider(transaction_title_provider)

        fake = Faker()

    def handle(self, *args, **options):
        self.seed_users()
        self.users = User.objects.all()
        self.stdout.write(self.style.SUCCESS('Users seeded'))

    def seed_users(self):
        self.stdout.write(self.style.SUCCESS('Seeding users'))
        bound_no = 0
        for bound in self.LEAGUE_BOUNDS:
            for i in range(self.USERS_PER_LEAGUE):
                self.create_user(bound)
                self.stdout.write(self.style.SUCCESS(
                    f'User {((bound_no * self.USERS_PER_LEAGUE) + i)} seeded'))
            bound_no += 1

    def create_user(self, bound):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = generate_email(first_name, last_name)
        points = randint(bound[0], bound[1])
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=self.DEFAULT_PASSWORD,
            points=points,
            is_active=True,
            is_staff=False,
            toggle_email='OFF'
        )
        user.set_password(self.DEFAULT_PASSWORD)
        self.add_default_categories(user)
        self.add_spending_categories(user)
        request_less_check_league(user)
        self.add_followings(user)

    def add_default_categories(self, user):
        self.stdout.write(self.style.SUCCESS(
            'Seeding default spending categories with transactions'))
        create_default_categories(user)
        user_default_categories = SpendingCategory.objects.filter(user=user)
        for category in user_default_categories:
            self.generate_transactions(category)

    def add_spending_categories(self, user):
        self.stdout.write(self.style.SUCCESS(
            'Seeding user spending categories with transactions'))
        for i in range(randint(1, 2)):
            name = self.faker.category_name()
            limit_amount = Decimal(randint(1, 25) * 100)
            limit = Limit.objects.create(
                limit_amount=limit_amount,
                start_date=date.today(),
                end_date=datetime.now() + timedelta(days=30),
                remaining_amount=limit_amount,
            )
            spending_category = SpendingCategory.objects.create(
                user=user, name=name, limit=limit)
            self.generate_transactions(spending_category)

    def generate_transactions(self, spending_category):
        num_transactions_per_month = randint(
            0, self.MAX_TRANSACTIONS_PER_CATEGORY_PER_MONTH)
        spending_category = get_object_or_404(
            SpendingCategory, id=spending_category.id)
        earliest_transaction_months_earlier = randint(
            1, self.MAX_START_OF_TRANSACTIONS_FOR_USER)
        for i in range(earliest_transaction_months_earlier):
            for j in range(num_transactions_per_month):
                title = self.faker.transaction_title()
                date = self.faker.date_between(
                    start_date='-{}y'.format(i), end_date='now')
                amount = generate_random_amount(
                    spending_category.limit.limit_amount//3)
                note = ""
                if random() < 0.5:
                    note = self.faker.sentence()

                transaction = SpendingTransaction.objects.create(
                    title=title,
                    date=date,
                    amount=amount,
                    spending_category=spending_category,
                    notes=note,
                )

    def add_followings(self, user):
        self.stdout.write(self.style.SUCCESS('Adding followings...'))
        all_users = list(User.objects.all())
        num_following = randint(0, len(all_users) - 1)
        random_users = sample(all_users, num_following)
        for random_user in random_users:
            user.toggle_follow(random_user)


def generate_email(first_name, last_name):
    return '{}.{}@from.seed'.format(first_name.lower(), last_name.lower())


def generate_random_amount(max_amount):
    return Decimal('%d.%d' % (randint(0, max_amount - 1), randint(0, 99)))
