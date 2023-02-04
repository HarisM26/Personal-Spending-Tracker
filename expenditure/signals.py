from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from decimal import *

@receiver(post_save,sender=Transaction)
def transaction_post_save_handler(instance,created,*args,**kwargs):
  current_user = instance.category.user
  if created:
    all_transactions = Transaction.objects.filter(category = instance.category)
    sum = 0
    for transaction in all_transactions:
      sum+=transaction.amount

    if sum >= (instance.category.limit*Decimal('0.90')) and sum < instance.category.limit :
      notification = create_notification(current_user,instance.category.limit,sum)
      print(notification.message)
    elif sum >= (instance.category.limit*Decimal('0.90')):
      notification = create_notification(current_user,instance.category.limit,sum)
      print(notification.message)

#to do add category_name
def create_notification(user,category_limit,sum):
  if sum >= (category_limit*Decimal('0.90')) and sum < category_limit:
    current_message = 'You are close to your limit. Please consider reducing your spending'
  else:
    current_message = 'You have reached your limit!'
  
  notification = Notification.objects.create(
    user_receiver = user,
    title = 'About your limit',
    message = current_message 
  )
  return notification
