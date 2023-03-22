from django.shortcuts import render
from expenditure.forms import *
from django.contrib.auth.decorators import login_required
from datetime import date
from expenditure.helpers import *
from django.contrib.auth.decorators import login_required
import expenditure.report_methods as rm


@login_required
def view_report(request):
    from_date = date(date.today().year-1, date.today().month, 1)
    to_date = date.today()
    current_user = request.user
    if request.method == "POST":
        form = DateReportForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data.get("from_date")
            to_date = form.cleaned_data.get("to_date")
    else:
        form = DateReportForm(initial={
            "from_date": from_date,
            "to_date": to_date
        })

    transactions = rm.get_total_transactions_by_date(
        current_user, from_date, to_date)
    largest_category = rm.get_the_category_with_the_largest_total_spending(
        current_user, from_date, to_date)
    close_categories = rm.get_list_of_categories_close_or_over_the_limit(
        current_user, from_date, to_date)
    list_of_categories_and_transactions = rm.get_list_of_transactions_in_category(
        current_user, from_date, to_date)
    range_categories = rm.get_categories_within_time_frame(
        current_user, from_date, to_date)
    average_daily_spending = rm.get_average_daily_spending_within_time_frame(
        current_user, from_date, to_date)
    income_categories_and_transactions = rm.get_list_of_transactions_in_income_category(
        current_user, from_date, to_date)

    context = {
        "from_date": from_date,
        "to_date": to_date,
        "form": form,
        "transactions": transactions,
        "close_categories": close_categories,
        'largest_category': largest_category,
        'list_of_categories_and_transactions': list_of_categories_and_transactions,
        'range_categories': range_categories,
        'average_daily_spending': average_daily_spending,
        'income_categories_and_transactions': income_categories_and_transactions,
    }
    return render(request, 'report.html', context=context)


def feed_page_report(request):
    current_user = request.user
    categories_within_limit = rm.total_categories_currently_within_limit(
        current_user)
    total_budget = rm.get_total_budget(current_user)  # not used yet
    remaining_budget = rm.get_total_remaining_budget(current_user)
    total_spending = rm.get_total_spending(current_user)
    total_income = rm.get_total_income(current_user)
    income_categories = rm.get_all_income_categories(current_user)
    context = {
        'categories_within_limit': categories_within_limit,
        'total_budget': total_budget,
        'remaining_budget': remaining_budget,
        'total_spending': total_spending,
        'total_income': total_income,
        'income_categories': income_categories,

    }
    return context
