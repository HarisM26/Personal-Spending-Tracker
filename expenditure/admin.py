from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SignUpForm
from .models import Profile
#from expenditure.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    model = User
    list_display = ("user_id","first_name", "last_name", "email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("first_name", "last_name","email", "password")}),
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
admin.site.register(Profile)
# Register your models here.
