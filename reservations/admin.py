from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Reservation)
class Reservation(admin.ModelAdmin):

    """ Reservation Admin Definition"""

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = (
        "status",
        # "in_progress",
        # "is_finished",
    )


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):
    list_display = ("day", "reservation")
