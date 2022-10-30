import strawberry
from typing import List, Optional
from rooms import types, queries


@strawberry.type
class Query:
    all_rooms: List[types.RoomType] = strawberry.field(
        resolver=queries.get_all_rooms,
    )

    room: Optional[types.RoomType] = strawberry.field(
        resolver=queries.get_room,
    )
