from django.conf import settings
import requests
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated
from medias.models import Photo


class GetUploadURL(APIView):
    def post(self, req):
        base_url = "https://api.cloudflare.com/client/"
        url = f"{base_url}v4/accounts/{settings.CF_ACCOUNT_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.CF_TOKEN}",
            },
        )
        one_time_url = one_time_url.json()
        result = one_time_url.get("result")
        uploadURL = result.get("uploadURL")
        id = result.get("id")

        return Response({"uploadURL": uploadURL, "id": id})


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
