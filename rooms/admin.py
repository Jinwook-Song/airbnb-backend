from django.contrib import admin

from rooms.models import Amenity, Room


@admin.action(description="Set all prices to zero")
def reset_prices(room_admin, request, querysets):
    for room in querysets.all():
        room.price = 0
        room.save()
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "rating",
        "total_amenities",
        "owner",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_allowed",
        "kind",
        "amenities",
    )

    search_fields = (
        "name",
        "^price",  # ^: startWith, default: contain
        "owner__username",
    )

    def total_amenities(self, room):
        return room.amenities.count()


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
