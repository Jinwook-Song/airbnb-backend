from django.db import models
from common.models import CommonModel

# Create your models here.


class Photo(CommonModel):
    """Photo model definition"""

    file = models.ImageField()
    description = models.CharField(max_length=150)
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return "Photo File"


class Video(CommonModel):
    """Video model definition"""

    file = models.FileField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return "Video File"
