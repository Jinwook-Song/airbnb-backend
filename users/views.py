import jwt
import requests
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
            return Response(
                {"error": "wrong passwrod"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            login(req, user)
            return Response(
                {"ok": "log-in succeed"},
                status=status.HTTP_200_OK,
            )


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


class GithubOAuth(APIView):
    def post(self, req):
        try:
            code = req.data.get("code")
            base_url = "https://github.com/login/oauth/access_token"
            client_id = "20d8b08eabc2559afc43"
            access_token = requests.post(
                f"{base_url}?code={code}&client_id={client_id}&client_secret={settings.GH_SECRET}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            user_emails = user_emails.json()

            try:
                user = User.objects.get(email=user_emails[0]["email"])
                login(req, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=user_emails[0]["email"],
                    name=user_data.get("name"),
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
                login(req, user)
                return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoOAuth(APIView):
    def post(self, req):
        try:
            code = req.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "c503f1bf93ea8c9971ff490a57332257",
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("progile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(req, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(req, user)
                return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
