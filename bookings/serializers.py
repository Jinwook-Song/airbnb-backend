from django.utils import timezone
from rest_framework import serializers
from bookings.models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):
    """
    Booking model에서 check_in, check_out 필드가 optional 하기떄문에
    오직 booking 생성을 위한 serializer
    """

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = [
            "check_in",
            "check_out",
            "guests",
        ]

    # custum validation method
    def validate_check_in(self, value):
        now = timezone.localtime().date()
        if value > now:
            return value
        else:
            raise serializers.ValidationError("Can't book in the past")

    def validate_check_out(self, value):
        now = timezone.localtime().date()
        if value > now:
            return value
        else:
            raise serializers.ValidationError("Can't book in the past")

    def validate(self, data):
        room = self.context.get("room")
        if data["check_in"] >= data["check_out"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out."
            )

        if Booking.objects.filter(
            room=room,
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of dates are already taken."
            )

        return data


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "pk",
            "check_in",
            "check_out",
            "guests",
        ]
