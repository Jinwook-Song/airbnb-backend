from django.db import models
from common.models import CommonModel

# Create your models here.


class ChatRoom(CommonModel):
    """Chat room definition"""

    participants = models.ManyToManyField("users.User")

    def __str__(self):
        return "Chatting Room"


class Message(CommonModel):
    """Message model definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    room = models.ForeignKey(
        "direct_messages.ChatRoom",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"
