import strawberry
from strawberry import auto
from users import models


@strawberry.django.type(models.User)
class UserType:
    name: auto
    email: auto
    username: auto
