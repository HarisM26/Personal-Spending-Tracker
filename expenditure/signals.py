from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from decimal import *
from expenditure.helpers import create_notification

@receiver(post_save,sender=Transaction)
def transaction_post_save_handler(instance,created,*args,**kwargs):
  current_user = instance.category.user
  if created and current_user.toggle_notification == 'ON' and instance.category.limit != None:
    all_transactions = Transaction.objects.filter(category = instance.category)
    total = Decimal('0.00')
    for transaction in all_transactions:
      total+=transaction.amount

    if total >= (instance.category.limit.calc_90_percent_of_limit) and \
              total < Decimal(instance.category.limit.limit_amount) :
      notification = create_notification(current_user,instance.category.name,instance.category.limit,total)
      notification.save()
    elif total >= (instance.category.limit.calc_90_percent_of_limit):
      notification = create_notification(current_user,instance.category.name,instance.category.limit,total)
      notification.save()      

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
