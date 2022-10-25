from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from wishlists.models import Wishlist
from wishlists.serializers import WishlistSerializer
from rooms.models import Room


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, req):
        all_wishlists = Wishlist.objects.filter(user=req.user)
        serializer = WishlistSerializer(
            all_wishlists,
            many=True,
            context={"req": req},
        )
        return Response(serializer.data)

    def post(self, req):
        serializer = WishlistSerializer(data=req.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=req.user)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, req, pk):
        wishlist = self.get_object(pk, req.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"req": req},
        )
        return Response(serializer.data)

    def delete(self, req, pk):
        wishlist = self.get_object(pk, req.user)
        wishlist.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, req, pk):
        wishlist = self.get_object(pk, req.user)
        serializer = WishlistSerializer(
            wishlist,
            data=req.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistToggle(APIView):
    def get_wishlist(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, req, pk, room_pk):
        wishilist = self.get_wishlist(pk, req.user)
        room = self.get_room(room_pk)

        if wishilist.rooms.filter(pk=room.pk).exists():
            wishilist.rooms.remove(room)
        else:
            wishilist.rooms.add(room)
        return Response(status=HTTP_200_OK)
