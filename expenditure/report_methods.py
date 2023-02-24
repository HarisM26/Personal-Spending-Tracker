from datetime import datetime, date, timedelta
from decimal import *
from django.db.models import Sum, F, IntegerField
from django.db.models.functions import TruncMonth, Cast, ExtractDay
from .models import *

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
        'weekly': 7,
        'monthly': 30,
        'yearly': 365,
    }

    categories_over_the_budget = []
    categories_close_to_the_budget = []

    for category in categories:
        limit_per_day = category.limit.limit_amount/periods_in_days[category.limit.time_limit_type]
        overall_budget = limit_per_day*days
        if category.total >= overall_budget:
            categories_over_the_budget.append(category)
        elif category.total >= overall_budget*Decimal(0.9):
            categories_close_to_the_budget.append(category)
        
    return categories_over_the_budget, categories_close_to_the_budget

def get_total_left_after_subtraction_of_essentail_spending():
    pass

def get_list_of_transactions_in_category(user, from_date, to_date):
    return SpendingTransaction.objects.select_related('spending_category').filter(
        date__gte=from_date,
        date__lte=to_date,
        spending_category__user=user
    )