from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from wishlists.models import WishList
from wishlists.serializers import WishlistSerializer


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, req):
        all_wishlists = WishList.objects.filter(user=req.user)
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
