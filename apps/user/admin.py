from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as ModelAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()


class UserAdmin(ModelAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    



admin.site.register(User, UserAdmin)


