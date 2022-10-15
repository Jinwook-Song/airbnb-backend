from rest_framework.views import APIView
from experiences.models import Perk
from experiences.serializers import PerkSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT


class Perks(APIView):
    def get(self, req):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, req):
        serializer = PerkSerializer(data=req.data)
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(PerkSerializer(new_amenity).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        amenity = self.get_object(pk=pk)
        serializer = PerkSerializer(amenity)
        return Response(serializer.data)

    def put(self, req, pk):
        amenity = self.get_object(pk=pk)
        serializer = PerkSerializer(amenity, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        amenity = self.get_object(pk=pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
