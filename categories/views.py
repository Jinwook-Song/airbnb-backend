from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):
    """Room Category View"""

    # TODO: Experience Category

    serializer_class = CategorySerializer
    queryset = Category.objects.filter(
        kind=Category.CategoryKindChoices.ROOMS,
    )
