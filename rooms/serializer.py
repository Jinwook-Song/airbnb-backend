from rest_framework.serializers import ModelSerializer
from rooms.models import Amenity, Room
from users.serializers import BriefUserSerializer
from categories.serializers import CategorySerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = [
            "name",
            "description",
        ]


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "pk",
            "name",
            "country",
            "city",
            "price",
        ]


class RoomSerializer(ModelSerializer):

    # populate: name, username, avatar
    owner = BriefUserSerializer(read_only=True)
    # populate: name, description
    amenities = AmenitySerializer(read_only=True, many=True)
    # populate: name, kind
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
