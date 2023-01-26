from django.db import models

class Notification(models.Model):
  #user_receiver = models.ForeignKey(User,on_delete=models.CASCADE)
  title = models.CharField(max_length=50, blank= False)
  message = models.CharField(max_length = 500, blank = False)
  status = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)

