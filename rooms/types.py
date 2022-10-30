from django.conf import settings
from typing import List, Optional
import strawberry
from strawberry import auto, types
from rooms.models import Room
from wishlists.models import Wishlist
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

    # type 명시는 필수적
    @strawberry.field
    def is_owner(self, info: types.Info) -> bool:
        return self.owner == info.context.request.user

    @strawberry.field
    def is_liked(self, info: types.Info) -> bool:
        return Wishlist.objects.filter(
            user=info.context.request.user,
            rooms__pk=self.pk,
        ).exists()
