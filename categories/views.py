from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT


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
            # if save called, automatically call create method
            # create method definition is our job
            new_category = serializers.save()
            serializers = CategorySerializer(new_category)
            return Response(serializers.data)
        else:
            return Response(serializers.errors)


@api_view(["GET", "PUT", "DELETE"])
def category(req, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound

    if req.method == "GET":
        serializers = CategorySerializer(category)
        return Response(serializers.data)
    elif req.method == "PUT":
        serializers = CategorySerializer(
            category,
            data=req.data,
            # because only for update
            partial=True,
        )
        if serializers.is_valid():
            # in this case, serializers call update method
            updated_category = serializers.save()
            serializers = CategorySerializer(updated_category)
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
    elif req.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
