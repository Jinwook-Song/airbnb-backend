from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from users.serializers import PrivateUserSerializer
from users.models import User


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, req):
        user = req.user
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, req):
        user = req.user
        serializer = PrivateUserSerializer(
            user,
            data=req.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, req):
        password = req.data.get("password")
        if not password:
            raise exceptions.ParseError("password is required.")

        serializer = PrivateUserSerializer(data=req.data)

        if serializer.is_valid():
            user = serializer.save()
            # hash the password
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    def get(self, req, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound
            # TODO: 공개할 정보만 선별
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)
