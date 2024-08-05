from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .tokens import get_tokens_for_user


class RegisterUser(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    "status": "success",
                    "message": "Registration successful",
                    "data": {
                        "accessToken": tokens.get("access"),
                        "user": {
                            "username": user.username,
                            "first_name": serializer.data["first_name"],
                            "last_name": serializer.data["last_name"],
                            "email": serializer.data["email"],
                        },
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            # serializer = self.serializer_class(user)
            tokens = get_tokens_for_user(user)
            return Response(
                {
                    "status": "success",
                    "message": "Login successful",
                    "data": {
                        "accessToken": tokens.get("access"),
                        "user": {
                            "username": user.username,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                        },
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            # Include validation errors in the response
            return Response(
                {
                    "status": "Bad Request",
                    "message": "Authentication failed",
                    "statusCode": 401,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
