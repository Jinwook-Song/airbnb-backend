from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST"])
def categories(req):
    if req.method == "GET":
        all_categories = Category.objects.all()
        serializers = CategorySerializer(all_categories, many=True)
        return Response(serializers.data)

    elif req.method == "POST":
        # Serializer know data shape
        serializers = CategorySerializer(data=req.data)
        if serializers.is_valid():
            return Response({"created": True})
        else:
            return Response(serializers.errors)


@api_view()
def categoriy(req, pk):
    category = Category.objects.get(pk=pk)
    serializers = CategorySerializer(category)
    return Response(serializers.data)
