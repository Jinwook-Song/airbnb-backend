from django.contrib import admin

from wishlists.models import WishList

# Register your models here.


@admin.register(WishList)
class Wishlist(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "created_at",
        "updated_at",
    )
