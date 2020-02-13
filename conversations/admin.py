from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Definition"""

    list_display = (
        "__str__",
        "count_massages",
        "count_participants",
    )

    filter_horizontal = [
        "participants",
    ]


@admin.register(models.Message)
class MassageAdmin(admin.ModelAdmin):

    """ Massage Admin Definition"""

    list_display = (
        "__str__",
        "created",
    )
