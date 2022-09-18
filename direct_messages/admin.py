from django.contrib import admin

from direct_messages.models import ChatRoom, Message


# Register your models here.


@admin.register(ChatRoom)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created_at",
        "updated_at",
    )

    list_filter = ("created_at",)


@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = (
        "text",
        "user",
        "room",
        "created_at",
    )

    list_filter = ("created_at",)
