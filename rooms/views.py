from rest_framework.views import APIView
from rooms.models import Amenity
from rooms.serializer import AmenitySerializer
from rest_framework.response import Response


class Amenities(APIView):
    def get(self, req):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, req):
        serializer = AmenitySerializer(data=req.data)
        if serializer.is_valid():
            new_amenity = serializer.save()
            return Response(AmenitySerializer(new_amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get(self, req, pk):
        pass

    def put(self, req, pk):
        pass

    def delete(self, req, pk):
        pass
