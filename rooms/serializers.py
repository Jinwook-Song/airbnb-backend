from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rooms.models import Amenity, Room
from users.serializers import BriefUserSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = [
            "name",
            "description",
        ]


class RoomListSerializer(ModelSerializer):

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        ]

    # method name is mandatory(get_[field])
    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        req = self.context["req"]
        return req.user == room.owner


class RoomSerializer(ModelSerializer):

    # populate: name, username, avatar
    owner = BriefUserSerializer(read_only=True)
    # populate: name, description
    # amenities = AmenitySerializer(read_only=True, many=True)
    # populate: name, kind
    category = CategorySerializer(read_only=True)

    rating = SerializerMethodField()
    is_owner = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    # Reverse Serializers
    # review has fk of room
    # room can access reviews pointing themself with related_name
    # reviews = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        exclude = ("amenities",)

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        req = self.context["req"]
        return req.user == room.owner
