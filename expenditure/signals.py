from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from decimal import *
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save,sender=Transaction)
def transaction_post_save_handler(instance,created,*args,**kwargs):
  current_user = instance.category.user
  if created and current_user.toggle_notification == 'ON':
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
      
def create_notification(user,category_name,category_limit_obj,total):
  if total >= (category_limit_obj.calc_90_percent_of_limit) and total < Decimal(category_limit_obj.limit_amount):
    current_message = f'{category_name} category close to its limit. Please consider reducing your spending'
  else:
    current_message = f'{category_name} category has reached its limit!'
  
  notification = Notification.objects.create(
    user_receiver = user,
    title = 'About your limit',
    message = current_message 
  )
  return notification

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
