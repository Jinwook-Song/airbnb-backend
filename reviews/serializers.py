from rest_framework import serializers
from reviews.models import Review
from users.serializers import BriefUserSerializer


class ReviewSerializer(serializers.ModelSerializer):

    user = BriefUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "user",
            "payload",
            "rating",
        ]
