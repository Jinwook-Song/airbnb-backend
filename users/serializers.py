from rest_framework.serializers import ModelSerializer
from users.models import User


class BriefUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "name",
            "username",
            "avatar",
        ]
