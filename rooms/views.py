from django.shortcuts import render
from rooms.models import Room


def see_all_rooms(req):
    rooms = Room.objects.all()
    return render(
        req,
        "all_rooms.html",
        {
            "title": "Comes from Django",
            "rooms": rooms,
        },
    )


def see_one_room(req, room_id):
    try:
        room = Room.objects.get(pk=room_id)
        return render(
            req,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            req,
            "room_detail.html",
            {
                "not_found": True,
            },
        )
