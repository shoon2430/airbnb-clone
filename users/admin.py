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
                    "avator",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
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
    )

    list_filter = UserAdmin.list_filter + ("superhost",)
