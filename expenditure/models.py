from django.db import models

class Notification(models.Model):
  STATUS_CHOICE=[('unread',('unread')),('read',('read'))]

  #user_receiver = models.ForeignKey(User,on_delete=models.CASCADE)
  title = models.CharField(max_length=300)
  message = models.CharField(max_length = 1200)
  status = models.CharField(max_length=6,choices=STATUS_CHOICE,default=1)
  time_created = models.TimeField(auto_now_add=True)
  date_created = models.DateField(auto_now_add=True)

class Limit(models.Model):
  LIMIT_STATUS=[('reached',('reached')),('not reached',('not reached')), ('approaching',('approaching'))]
  limit_amount = models.DecimalField(max_digits=10,decimal_places=2)
  spent_amount = models.DecimalField(max_digits=10,decimal_places=2)
  status = models.CharField(choices=LIMIT_STATUS, default='not reached')
  