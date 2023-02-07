from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name','limit')
admin.site.register(Category,CategoryAdmin)

class TransactionAdmin(admin.ModelAdmin):
  list_display = ('title','amount','category')
admin.site.register(Transaction,TransactionAdmin)

class NotificationAdmin(admin.ModelAdmin):
  list_display = ('user_receiver','message','status')
admin.site.register(Notification,NotificationAdmin)


class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    model = User
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(User, CustomUserAdmin)
# Register your models here.

