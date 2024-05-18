from typing import Any
from django.db import models
from django.contrib.auth.models import User

import datetime

# Create your models here.


"""
class Conversation(models.Model):
    From = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="conversations",
    )
    to = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="_conversations",
    )

    date = models.DateTimeField(auto_now=True)
"""


class Message(models.Model):
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.PROTECT,
        related_name="messages",
    )
    """
    sender = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="sent_messages",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="received_messages",
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.sender.username} to {self.receiver.username} at {self.date}"


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # self.conversation.date = datetime.datetime.now()
        # self.conversation.save()


