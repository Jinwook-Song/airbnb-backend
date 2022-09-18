from django.db import models
from common.models import CommonModel

# Create your models here.


class Booking(CommonModel):
    """Booking model definition"""

    class BookingKindChoices(models.TextChoices):
        ROOM = ("room", "Room")
        EXPERIENCE = ("expertise", "Expertise")

    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    # room(또는 experience)이 삭제되더라도
    # user는 자신의 예약 내역을 확인할 수 있도록 SET_NULL
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Common
    guests = models.PositiveIntegerField()

    # For room
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)

    # For experience
    experience_time = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.kind.title()} / {self.user}"
