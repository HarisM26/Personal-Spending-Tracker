from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm


admin.site.register(Limit)

class SpendingCategoryAdmin(admin.ModelAdmin):
  list_display = ('name', Limit)
admin.site.register(SpendingCategory,SpendingCategoryAdmin)

class IncomeCategoryAdmin(admin.ModelAdmin):
   list_display = ('name',)
admin.site.register(IncomeCategory, IncomeCategoryAdmin)

class TransactionAdmin(admin.ModelAdmin):
  list_display = ('title','amount','spending_category')
admin.site.register(SpendingTransaction,TransactionAdmin)

class NotificationAdmin(admin.ModelAdmin):
  list_display = ('user_receiver','message','status')
admin.site.register(Notification,NotificationAdmin)

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    model = User
    list_display = ("email", "is_staff", "is_active","id")
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email","password", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)

