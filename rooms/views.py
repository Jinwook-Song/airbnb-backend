from django.db import transaction
from rest_framework.views import APIView
from rooms.models import Amenity, Room
from rooms.serializer import AmenitySerializer, RoomListSerializer, RoomSerializer
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from categories.models import Category
from reviews.serializers import ReviewSerializer


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
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        amenity = self.get_object(pk=pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, req, pk):
        amenity = self.get_object(pk=pk)
        serializer = AmenitySerializer(amenity, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        amenity = self.get_object(pk=pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, req):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"req": req},
        )
        return Response(serializer.data)

    def post(self, req):
        if req.user.is_authenticated:
            serializer = RoomSerializer(data=req.data)
            if serializer.is_valid():
                category_pk = req.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be rooms.")
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")
                try:
                    with transaction.atomic():
                        room = serializer.save(owner=req.user, category=category)
                        amenities = req.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                        return Response(
                            RoomSerializer(
                                room,
                                context={"req": req},
                            ).data,
                        )
                except Exception:
                    raise ParseError("Amenity not found.")
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        room = self.get_object(pk)
        serializer = RoomSerializer(
            room,
            context={"req": req},
        )
        return Response(serializer.data)

    def put(self, req, pk):
        room = self.get_object(pk)
        if not req.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != req.user:
            raise PermissionDenied

        serializer = RoomSerializer(room, data=req.data, partial=True)
        if serializer.is_valid():
            category_pk = req.data.get("category")
            amenities = req.data.get("amenities")

            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be rooms.")
                except Category.DoesNotExist:
                    raise ParseError("Category not found.")

            try:
                with transaction.atomic():
                    if category_pk:
                        serializer.save(category=category)
                    else:
                        serializer.save()

                    if amenities:
                        room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)

                    return Response(
                        RoomSerializer(
                            room,
                            context={"req": req},
                        ).data,
                    )
            except Exception as e:
                raise ParseError(e)

        else:
            return Response(serializer.errors)

    def delete(self, req, pk):
        room = self.get_object(pk)
        if not req.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != req.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        try:
            page = req.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        take = 5
        start = (page - 1) * take
        end = page * take

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        try:
            page = req.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        take = 5
        start = (page - 1) * take
        end = page * take

        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)
