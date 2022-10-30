import strawberry
from strawberry import auto
from rooms.models import Room
from users import types


@strawberry.django.type(Room)
class RoomType:
    id: auto
    name: auto
    kind: auto
    owner: "types.UserType"
