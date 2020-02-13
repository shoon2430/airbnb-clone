from django.db import models
from core import models as core_models

# Create your models here.


class Conversation(core_models.TimeStampModel):

    participants = models.ManyToManyField("users.User", blank=True)

    def __str__(self):
        users = self.participants.all()
        usernames = []
        for user in users:
            usernames.append(user.username)

        return ", ".join(usernames)

    def count_massages(self):
        return self.messages.count()

    count_massages.short_description = "NUMER MASSAGES"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "NUMER PARTICIPANTS"


class Message(core_models.TimeStampModel):

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
