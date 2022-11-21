from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from categories.models import Category
from rooms.models import Amenity, Room
from rooms.serializers import AmenitySerializer, RoomListSerializer, RoomSerializer
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


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

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, req):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"req": req},
        )
        return Response(serializer.data)

    def post(self, req):
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


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

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
        if room.owner != req.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

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

        take = settings.TAKE_SIZE
        start = (page - 1) * take
        end = page * take

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, req, pk):
        serializer = ReviewSerializer(data=req.data)
        if serializer.is_valid():
            review = serializer.save(
                user=req.user,
                room=self.get_object(pk),
            )
            return Response(ReviewSerializer(review).data)
        else:
            return Response(serializer.errors)


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

        take = settings.TAKE_SIZE
        start = (page - 1) * take
        end = page * take

        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, req, pk):
        room = self.get_object(pk)
        if req.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerializer(data=req.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        room = self.get_object(pk)
        now = timezone.localtime().date()
        print(now)
        # room pk를 통해 bookings을 가져올 수도 있다.
        # 하지만 이 경우, room이 존재 하지 않는 경우와 booking이 존재하지 않는 경우가
        # 동일하게 빈 배열을 return 하게된다.
        # bookings = Booking.objects.filter(room__pk=pk)
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, req, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=req.data)
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=req.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            return Response(PublicBookingSerializer(booking).data)
        else:
            return Response(serializer.errors)
