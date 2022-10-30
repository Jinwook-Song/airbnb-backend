from strawberry.types import Info
from strawberry.permission import BasePermission
from typing import Any


class OnlyLoggedIn(BasePermission):

    message = "Log in first"

    def has_permission(self, source: Any, info: Info, **kwards):
        return info.context.request.user.is_authenticated
