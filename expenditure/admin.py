from django.contrib import admin
from expenditure.models.limit import Limit
from expenditure.models.categories import SpendingCategory, IncomeCategory
from expenditure.models.transactions import SpendingTransaction, IncomeTransaction
from expenditure.models.notification import Notification
from expenditure.models.user import Profile  # User
from django.contrib.auth.admin import UserAdmin
from .forms import SignUpForm
from django.contrib.auth import get_user_model
User = get_user_model()

admin.site.register(Limit)


class SpendingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', Limit)


admin.site.register(SpendingCategory, SpendingCategoryAdmin)


class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(IncomeCategory, IncomeCategoryAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'spending_category')


admin.site.register(SpendingTransaction, TransactionAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_receiver', 'message', 'status')


admin.site.register(Notification, NotificationAdmin)


class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    model = User
    list_display = ("user_id", "first_name", "last_name",
                    "email", "is_staff", "is_active", "points")

    list_filter = ("email", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "email", "password", "points",)}),
        ("Permissions", {"fields": ("is_staff",
         "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password", "is_staff",
                "is_active", "groups", "user_permissions", "points",
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
