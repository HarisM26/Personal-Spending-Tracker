from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from decimal import *

@receiver(post_save,sender=Transaction)
def transaction_post_save_handler(sender,instance,created,*args,**kwargs):
  sender = instance.category.user
  if created:
    all_transactions = Transaction.objects.filter(category = instance.category)
    sum = 0
    for _ in all_transactions:
      sum+=_.amount

    if sum >= (instance.category.limit*Decimal('0.90')) and sum < instance.category.limit :
      notification = create_notification(sender,instance.category.limit,sum)
      print(notification.message)
    elif sum >= (instance.category.limit*Decimal('0.90')):
      notification = create_notification(sender,instance.category.limit,sum)
      print(notification.message)

def create_notification(user,category_limit,sum):
  current_message = ''
  if sum >= (category_limit*Decimal('0.90')) and sum < category_limit:
    current_message = 'You close to your limit. Please consider reducing your spending'
  else:
    current_message = 'You have reached your limit!'
  
  notification = Notification.objects.create(
    user_receiver = user,
    title = 'About your limit',
    message = current_message 
  )
  return notification
