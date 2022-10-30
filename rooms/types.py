from django.conf import settings
from typing import List, Optional
import strawberry
from strawberry import auto
from rooms.models import Room
from users.types import UserType
from reviews.types import ReviewType


@strawberry.django.type(Room)
class RoomType:
    id: auto
    name: auto
    kind: auto
    owner: UserType

    @strawberry.field
    def reviews(self, page: Optional[int] = 1) -> List[ReviewType]:
        # self == room
        take = settings.TAKE_SIZE
        start = (page - 1) * take
        end = page * take
        return self.reviews.all()[start:end]

    @strawberry.field
    def rating(self) -> str:
        # self == room
        return self.rating()
