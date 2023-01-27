from django.db import models

class Notification(models.Model):
  #user_receiver = models.ForeignKey(User,on_delete=models.CASCADE)
  title = models.CharField(max_length=300, blank= False)
  message = models.CharField(max_length = 1200, blank = False)
  status = models.BooleanField(default=False)
  time_created = models.TimeField(auto_now_add=True, blank=False)
  date_created = models.DateField(auto_now_add=True, blank=False)

