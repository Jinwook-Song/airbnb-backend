from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
