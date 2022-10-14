from categories.models import Category
from categories.serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT


class Categories(APIView):
    def get(self, req):
        all_categories = Category.objects.all()
        serializers = CategorySerializer(all_categories, many=True)
        return Response(serializers.data)

    def post(self, req):
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


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        serializers = CategorySerializer(self.get_object(pk))
        return Response(serializers.data)

    def put(self, req, pk):
        serializers = CategorySerializer(
            self.get_object(pk),
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

    def delete(self, req, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
