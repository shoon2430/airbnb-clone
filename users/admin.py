from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


# Register your models here.


class RoomInline(admin.TabularInline):
    model = models.room_models.Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin"""

    inlines = (RoomInline,)

    USERADMIN_FIELDS = UserAdmin.fieldsets
    COSTOM_FIELDS = (
        (
            "CostomFields",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "login_method",
                )
            },
        ),
    )

    fieldsets = USERADMIN_FIELDS + COSTOM_FIELDS

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )

    list_filter = UserAdmin.list_filter + ("superhost",)
