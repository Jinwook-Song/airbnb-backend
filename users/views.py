import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions, status
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


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, req):
        user = req.user
        old_password = req.data.get("old_password")
        new_password = req.data.get("new_password")

        if not old_password or not new_password:
            raise exceptions.ParseError

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.ParseError


class LogIn(APIView):
    def post(self, req):
        username = req.data.get("username")
        password = req.data.get("password")

        if not username or not password:
            raise exceptions.ParseError

        user = authenticate(
            req,
            username=username,
            password=password,
        )

        if not user:
            return Response({"error": "wrong passwrod"})
        else:
            login(req, user)
            return Response({"ok": "log-in succeed"})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, req):
        logout(req)
        return Response({"ok": "log-out succeed"})


class JWTLogin(APIView):
    def post(self, req):
        username = req.data.get("username")
        password = req.data.get("password")

        if not username or not password:
            raise exceptions.ParseError

        user = authenticate(
            req,
            username=username,
            password=password,
        )

        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong passwrod"})
