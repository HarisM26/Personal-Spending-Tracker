from decimal import *
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import *


def get_total_transactions_by_date(user, from_date, to_date):
    return SpendingTransaction.objects.filter(
        date__gte=from_date,
        date__lte=to_date,
        spending_category__user=user
    ).annotate(month=TruncMonth("date")).values("month").annotate(total=Sum("amount")).values("month", "total")


def get_the_category_with_the_largest_total_spending(user, from_date, to_date):
    largest_category = SpendingCategory.objects.prefetch_related('transactions').filter(
        user=user,
        transactions__date__gte=from_date,
        transactions__date__lte=to_date,
    ).annotate(
        month=TruncMonth("transactions__date")
    ).annotate(
        total=Sum("transactions__amount")
    ).order_by("-total")

    if largest_category:
        return largest_category.first()


def get_categories_within_time_frame(user, from_date, to_date):
    categories = SpendingCategory.objects.prefetch_related('transactions').filter(
        user=user,
        transactions__date__gte=from_date,
        transactions__date__lte=to_date,
    ).annotate(
        total=Sum("transactions__amount")
    ).order_by("-total")

    return categories


def get_all_income_categories(user):
    categories = IncomeCategory.objects.prefetch_related('transactions').filter(
        user=user
    ).annotate(
        total=Sum("transactions__amount")
    ).order_by("-total")

    return categories


def get_average_daily_spending_within_time_frame(user, from_date, to_date):
    days = (to_date-from_date).days
    categories = get_categories_within_time_frame(user, from_date, to_date)

    total_transactions = 0
    for category in categories:
        total_transactions += category.total
    if days != 0:
        return total_transactions/days
    else:
        return total_transactions


def get_list_of_categories_close_or_over_the_limit(user, from_date, to_date):
    days = (to_date-from_date).days
    categories = SpendingCategory.objects.prefetch_related('transactions').select_related('limit').filter(
        user=user,
        transactions__date__gte=from_date,
        transactions__date__lte=to_date,
    ).annotate(
        month=TruncMonth("transactions__date")
    ).annotate(
        total=Sum("transactions__amount")
    )
    periods_in_days = {
        'daily': 1,
        'weekly': 7,
        'monthly': 30,
        'yearly': 365,
    }

    categories_over_the_budget = []
    categories_close_to_the_budget = []

    for category in categories:
        limit_per_day = category.limit.limit_amount / \
            periods_in_days[category.limit.time_limit_type]
        overall_budget = limit_per_day*days
        if category.total >= overall_budget:
            categories_over_the_budget.append(category)
        elif category.total >= overall_budget*Decimal(0.9):
            categories_close_to_the_budget.append(category)

    return categories_over_the_budget, categories_close_to_the_budget

def get_list_of_transactions_in_category(user, from_date, to_date):
    return SpendingTransaction.objects.select_related('spending_category').filter(
        date__gte=from_date,
        date__lte=to_date,
        spending_category__user=user
    ).annotate(month=TruncMonth("date")).annotate(total=Sum("amount")).order_by("-date")


def total_categories_currently_within_limit(user):
    all_spending_categories = SpendingCategory.objects.filter(user=user)
    categories_within_limit = []
    for category in all_spending_categories:
        if category.limit.status != 'reached':
            categories_within_limit.append(category)
    return len(categories_within_limit)


def get_total_budget(user):
    all_spending_categories = SpendingCategory.objects.filter(user=user)
    total_budget = 0
    for category in all_spending_categories:
        total_budget += category.limit.limit_amount

    return total_budget


def get_total_remaining_budget(user):
    all_spending_categories = SpendingCategory.objects.filter(user=user)
    remaining_budget = 0
    for category in all_spending_categories:
        remaining_budget += category.limit.remaining_amount

    return remaining_budget


def get_total_spending(user):
    total_budget = get_total_budget(user)
    remaining_budget = get_total_remaining_budget(user)
    total_spending = total_budget - remaining_budget
    return total_spending


def get_total_income(user):
    all_income = IncomeTransaction.objects.filter(income_category__user=user)
    total_income = 0

    for income in all_income:
        total_income += income.amount

    return total_income
