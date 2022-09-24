from django.db import models

from common.models import CommonModel

# Create your models here.


class Experience(CommonModel):
    """Experience model definition"""

    country = models.CharField(max_length=50, default="Korea")
    city = models.CharField(max_length=50, default="Seoul")
    name = models.CharField(max_length=250)
    description = models.TextField()
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    price = models.PositiveBigIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    perks = models.ManyToManyField(
        "experiences.Perk",
        related_name="experiences",
    )
    # Category가 삭제되면 Experience의 Category는 Null
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )

    def __str__(self) -> str:
        return self.name


class Perk(CommonModel):
    """What is included in the experiences"""

    name = models.CharField(max_length=100)
    details = models.CharField(max_length=250, blank=True, default="")
    description = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return self.name
