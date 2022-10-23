from rest_framework.views import APIView
from medias.models import Photo
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated


class PhotoDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, req, pk):
        photo = self.get_object(pk)
        if (photo.room and photo.room.owner != req.user) or (
            photo.experience and photo.experience.host != req.user
        ):
            raise PermissionDenied
        pass
        photo.delete()
        return Response(status=HTTP_204_NO_CONTENT)
