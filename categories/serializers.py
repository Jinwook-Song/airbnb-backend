from rest_framework import serializers


class CategorySerializer(serializers.Serializer):

    # Customizable
    # How & What
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    kind = serializers.CharField()
