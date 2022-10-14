from rest_framework import serializers
from categories.models import Category


class CategorySerializer(serializers.Serializer):

    # Customizable
    # How & What
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    kind = serializers.ChoiceField(
        choices=Category.CategoryKindChoices.choices,
    )
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # python unpacking
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # second args return defualt value
        instance.name = validated_data.get("name", instance.name)
        instance.kind = validated_data.get("kind", instance.kind)
        instance.save()
        return instance
