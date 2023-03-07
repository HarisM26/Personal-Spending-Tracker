from django.db.models.signals import post_save, post_delete
from .models import *
from django.dispatch import receiver
from decimal import *
from expenditure.helpers import create_limit_notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_delete, sender=IncomeTransaction)
def remove_incometransaction_points(instance, *args, **kwargs):
    current_user = instance.income_category.user
    current_user.points -= 3
    current_user.save()

@receiver(post_save, sender=SpendingTransaction)
def update_remaining_amount(instance, created, *args, **kwargs):
    # order matters- update remaining amount first
    if created:
        all_transactions = SpendingTransaction.objects.filter(
            spending_category=instance.spending_category, is_current=True)
        total = Decimal('0.00')
        for transaction in all_transactions:
            total += transaction.amount

        limit = instance.spending_category.limit
        limit.remaining_amount = limit.limit_amount-total
        limit.save()


@receiver(post_save, sender=SpendingTransaction)
def transaction_post_save_handler(instance, created, *args, **kwargs):
    current_user = instance.spending_category.user
    if created and current_user.toggle_notification == 'ON':
        # filter current transactions in particular category
        all_transactions = SpendingTransaction.objects.filter(
            spending_category=instance.spending_category, is_current=True)
        total = Decimal('0.00')
        for transaction in all_transactions:
            total += transaction.amount

        if total >= (instance.spending_category.limit.calc_90_percent_of_limit) and \
                total < Decimal(instance.spending_category.limit.limit_amount):
            notification = create_limit_notification(
                current_user, instance.spending_category.name, instance.spending_category.limit, total)
            notification.save()
            limit = instance.spending_category.limit
            limit.status = 'approaching'
            limit.save()
        elif total >= (instance.spending_category.limit.calc_90_percent_of_limit):
            notification = create_limit_notification(
                current_user, instance.spending_category.name, instance.spending_category.limit, total)
            notification.save()
            limit = instance.spending_category.limit
            limit.status = 'reached'
            limit.save()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
