from django.contrib import admin

from reviews.models import Review


class WorldFilter(admin.SimpleListFilter):
    title = "Filter by words"

    # URL Query
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, queryset):
        word = self.value()
        if word:
            return queryset.filter(payload__contains=word)
        else:
            queryset


class RatingFilter(admin.SimpleListFilter):
    title = "Filter by 🌟x3"

    parameter_name = "star"

    def lookups(self, request, model_admin):
        return [
            ("3", "🌟x3 👆"),
        ]

    def queryset(self, request, queryset):
        stars = self.value()
        if stars:
            return queryset.filter(rating__gte=stars)
        else:
            queryset


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("__str__", "payload")

    list_filter = (
        WorldFilter,
        RatingFilter,
        "rating",
        "user__is_host",
        "room__category__kind",
    )
