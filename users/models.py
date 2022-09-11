from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class Genders(models.TextChoices):
        MALE = ("male", "Male")  # database value, admin pannel label
        FEMALE = ("female", "Female")

    class Languagues(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class Currencies(models.TextChoices):
        KRW = ("krw", "Korean ₩")
        USD = ("usd", "Dollar $")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    name = models.CharField(
        max_length=150,
        default="",
    )
    avatar = models.ImageField(
        blank=True,  # blank는 database가 아닌 form level이다.
    )
    is_host = models.BooleanField(
        default=False,
    )
    gender = models.CharField(
        max_length=10,
        choices=Genders.choices,
        default=Genders.MALE,
    )
    language = models.CharField(
        max_length=2,
        choices=Languagues.choices,
        default=Languagues.KR,
    )
    currency = models.CharField(
        max_length=3,
        choices=Currencies.choices,
        default=Currencies.KRW,
    )
