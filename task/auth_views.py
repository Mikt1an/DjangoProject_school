from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .auth_serializers import RegisterSerializer


ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"


def set_auth_cookies(response, access, refresh):
    response.set_cookie(
        key=ACCESS_COOKIE,
        value=str(access),
        httponly=True,
        secure=False,
        samesite="Lax",
    )

    response.set_cookie(
        key=REFRESH_COOKIE,
        value=str(refresh),
        httponly=True,
        secure=False,
        samesite="Lax",
    )


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.save()

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {
                    "detail": (
                        "Username and password are required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            request=request,
            username=username,
            password=password,
        )

        if user is None:
            return Response(
                {
                    "detail": "Invalid credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response(
            {
                "detail": "Login successful.",
            },
            status=status.HTTP_200_OK,
        )

        set_auth_cookies(
            response,
            access,
            refresh,
        )

        return response


class RefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(
            REFRESH_COOKIE
        )

        if not refresh_token:
            return Response(
                {
                    "detail": "Refresh token is missing."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token

        except Exception:
            return Response(
                {
                    "detail": "Invalid refresh token."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {
                "detail": "Access token refreshed.",
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key=ACCESS_COOKIE,
            value=str(access),
            httponly=True,
            secure=False,
            samesite="Lax",
        )

        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(
            REFRESH_COOKIE
        )

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        response = Response(
            {
                "detail": "Logout successful.",
            },
            status=status.HTTP_200_OK,
        )

        response.delete_cookie(ACCESS_COOKIE)
        response.delete_cookie(REFRESH_COOKIE)

        return response