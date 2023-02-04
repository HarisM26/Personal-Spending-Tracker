from expenditure.models import Transaction
from django import template

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
