from django.http import HttpResponse


def see_all_rooms(req):
    return HttpResponse("see all rooms")


def see_one_room(req, room_id):
    return HttpResponse(f"see {room_id} room")
