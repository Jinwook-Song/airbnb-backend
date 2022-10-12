from django.urls import path
from rooms import views


urlpatterns = [
    path("", views.see_all_rooms),  # root
    path("<int:room_id>", views.see_one_room),  # root
]
