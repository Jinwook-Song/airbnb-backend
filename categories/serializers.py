from rest_framework import serializers


class CategorySerializer(serializers.Serializer):

    # Customizable
    # How & What
    pk = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    kind = serializers.CharField()
