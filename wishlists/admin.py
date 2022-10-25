from django.contrib import admin

from wishlists.models import Wishlist

# Register your models here.


@admin.register(Wishlist)
class Wishlist(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "created_at",
        "updated_at",
    )
