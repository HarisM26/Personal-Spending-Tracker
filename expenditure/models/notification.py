from django.db import models
from django.utils.translation import gettext_lazy as _
from expenditure.choices import *
from expenditure.models.user import User


class Notification(models.Model):
    user_receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    message = models.CharField(max_length=1200)
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICE, default='unread')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.message
