import strawberry
from strawberry import auto
from rooms.models import Room


@strawberry.django.type(Room)
class RoomType:
    id: auto
    name: auto
    kind: auto
