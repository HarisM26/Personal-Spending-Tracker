from django.contrib import admin
from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name','limit')

class TransactionAdmin(admin.ModelAdmin):
  list_display = ('description','amount','category')

class NotificationAdmin(admin.ModelAdmin):
  list_display = ('user_receiver','message','status')

admin.site.register(User)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(Notification,NotificationAdmin)