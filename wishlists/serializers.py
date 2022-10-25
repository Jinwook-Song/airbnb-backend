from rest_framework.serializers import ModelSerializer
from wishlists.models import WishList
from rooms.serializers import RoomListSerializer


class WishlistSerializer(ModelSerializer):

    rooms = RoomListSerializer(many=True, read_only=True)

    class Meta:
        model = WishList
        fields = [
            "name",
            "rooms",
        ]
