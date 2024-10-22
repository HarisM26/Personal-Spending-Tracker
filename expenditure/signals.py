from django.db.models.signals import post_save, post_delete, pre_delete
from .models import *
from django.dispatch import receiver
from decimal import *
from expenditure.helpers import create_limit_notification
from django.contrib.auth import get_user_model
from expenditure.models.categories import *
from expenditure.models.transactions import *
from expenditure.models.user import *
from .email_manager import EmailSender
from .helpers import get_percentage_of_limit_used

User = get_user_model()


@receiver(post_delete, sender=IncomeTransaction)
def remove_incometransaction_points(instance, *args, **kwargs):
    POINTS = instance.get_points()
    current_user = instance.income_category.user
    current_user.points -= POINTS
    current_user.save()

@receiver(post_delete, sender=SpendingTransaction)
def remove_spendingtransaction_points(instance, *args, **kwargs):
    current_user = instance.spending_category.user
    POINTS = instance.get_points()
    instance.spending_category.limit.remaining_amount += instance.amount
    instance.spending_category.limit.save()
    current_user.points -= POINTS
    current_user.save()

@receiver(pre_delete, sender=IncomeCategory)
def remove_incomecategory_and_its_transactions(instance, *args, **kwargs):
    all_transactions = IncomeTransaction.objects.filter(
            income_category=instance)
    for transaction in all_transactions:
        transaction.delete()

@receiver(pre_delete, sender=SpendingCategory)
def remove_spendingcategory_and_its_transactions(instance, *args, **kwargs):
    all_transactions = SpendingTransaction.objects.filter(
            spending_category=instance)
    for transaction in all_transactions:
        transaction.delete()


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


@receiver(post_save, sender=SpendingCategory)
def update_remaining_when_category_edited(instance, created, *args, **kwargs):
    if not created:
        all_transactions = SpendingTransaction.objects.filter(
            spending_category=instance, is_current=True)
        total = Decimal('0.00')
        for transaction in all_transactions:
            total += transaction.amount

        limit = instance.limit
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
            EmailSender().send_approaching_limit_email(current_user, instance.spending_category.name,
                                                       get_percentage_of_limit_used(instance.spending_category.limit))
            limit = instance.spending_category.limit
            limit.status = 'approaching'
            limit.save()
        elif total >= (instance.spending_category.limit.calc_90_percent_of_limit):
            notification = create_limit_notification(
                current_user, instance.spending_category.name, instance.spending_category.limit, total)
            notification.save()
            EmailSender().send_reached_limit_email(
                current_user, instance.spending_category.name)
            limit = instance.spending_category.limit
            limit.status = 'reached'
            limit.save()


@receiver(post_save, sender=SpendingCategory)
def category_post_save_handler(instance, created, *args, **kwargs):
    current_user = instance.user
    if not created and current_user.toggle_notification == 'ON':
        # filter current transactions in particular category
        all_transactions = SpendingTransaction.objects.filter(
            spending_category=instance, is_current=True)
        total = Decimal('0.00')
        for transaction in all_transactions:
            total += transaction.amount

        if total >= (instance.limit.calc_90_percent_of_limit) and \
                total < Decimal(instance.limit.limit_amount):
            notification = create_limit_notification(
                current_user, instance.name, instance.limit, total)
            notification.save()
            EmailSender().send_approaching_limit_email(current_user, instance.name,
                                                       get_percentage_of_limit_used(instance.limit))
            limit = instance.limit
            limit.status = 'approaching'
            limit.save()
        elif total >= (instance.limit.calc_90_percent_of_limit):
            notification = create_limit_notification(
                current_user, instance.name, instance.limit, total)
            notification.save()
            EmailSender().send_reached_limit_email(
                current_user, instance.name)
            limit = instance.limit
            limit.status = 'reached'
            limit.save()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()