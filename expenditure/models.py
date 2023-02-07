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
  TIME_LIMIT_TYPE=[('weekly',('weekly')),('monthly',('monthly')),('yearly',('yearly'))]

  limit_amount = models.DecimalField(max_digits=10,decimal_places=2)
  spent_amount = models.DecimalField(max_digits=10,decimal_places=2)
  status = models.CharField(max_length=50, choices=LIMIT_STATUS, default='not reached')
  time_limit_type = models.CharField(max_length=50, choices=TIME_LIMIT_TYPE, default='weekly')
  start_date = models.DateField()
  end_date = models.DateField()
 


  def update_status(self):
    used_percent = self.get_percentage_of_limit_used()
    if used_percent >= 1.0:
      self.status = 'reached'
    elif used_percent >= 0.9:
      self.status = 'approaching'
    else:
      self.status ='not reached'
  
  def get_percentage_of_limit_used(self):
    return self.spent_amount/self.limit_amount

  def save(self, *args, **kwargs):
    self.update_status()
    super(Limit, self).save(*args, **kwargs)


  