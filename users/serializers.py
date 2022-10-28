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


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            # only admin pannel
            "groups",
            "user_permissions",
        ]
