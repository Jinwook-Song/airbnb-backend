from django.shortcuts import render
from django.http import HttpResponse
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
    return HttpResponse(f"see {room_id} room")
