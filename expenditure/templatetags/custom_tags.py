from expenditure.models.transactions import SpendingTransaction, IncomeTransaction
from expenditure.models.notification import Notification
from django import template
from datetime import datetime


register = template.Library()


@register.filter
def get_spending_transactions(category):
    transactions = SpendingTransaction.objects.filter(
        spending_category=category)
    return transactions


@register.filter
def get_income_transactions(category):
    transactions = IncomeTransaction.objects.filter(income_category=category)
    return transactions


@register.filter
def get_transaction_total(iterable):
    total = 0
    for element in iterable:
        if element.is_current:
            total += element.amount
    return total


@register.filter
def get_income_transaction_total(iterable):
    total = 0
    for element in iterable:
        total += element.amount
    return total


@register.filter
def get_article_dict_element(dict, key):
    return dict[f'{key}']

# change date format to eg. 01 January, 2000


@register.filter
def convert_date(date):
    dt = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    return dt.strftime('%d %B, %Y')


@register.filter
def to_2_decimal_places(value):
    return round(value, 2)

# Greetings custom tag


@register.filter
def get_greetings(date):
    pass


@register.filter
def get_month(monthvalue):
    months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December']
    return months[monthvalue]


@register.filter
def get_latest_transaction_month(lst):
    return lst[0].date.month


@register.filter
def get_latest_transaction_year(lst):
    return lst[0].date.year
