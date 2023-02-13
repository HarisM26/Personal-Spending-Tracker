from expenditure.models import Transaction
from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_transactions(category):
  transactions = Transaction.objects.filter(category=category)
  return transactions

@register.filter
def get_transaction_total(iterable):
  total = 0
  for element in iterable:
    total+=element.amount
  return total

@register.filter
def get_article_dict_element(dict, key):
  return dict[f'{key}']

@register.filter
def convert_date(date):
  dt = datetime.strptime(date,'%Y-%m-%dT%H:%M:%SZ')
  return dt.strftime('%d %B, %Y')