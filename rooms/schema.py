import strawberry
from typing import List, Optional
from rooms import types, queries
from common.permissions import OnlyLoggedIn


@strawberry.type
class Query:
    all_rooms: List[types.RoomType] = strawberry.field(
        resolver=queries.get_all_rooms,
        permission_classes=[OnlyLoggedIn],
    )

    room: Optional[types.RoomType] = strawberry.field(
        resolver=queries.get_room,
    )
