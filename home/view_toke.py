from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializer import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serialiser = RegisterSerializer(data=data)

        if not serialiser.is_valid():
            return Response(
                {"status": "error", "message": serialiser.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serialiser.save()
        return Response(
            {"status": "success", "message": "User Created"},
            status=status.HTTP_201_CREATED,
        )


class AuthAPI(APIView):
    def post(self, request):
        data = request.data
        serialiser = LoginSerializer(data=data)
        if not serialiser.is_valid():
            return Response(
                {"status": "error", "message": serialiser.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        print(serialiser.data)
        user = authenticate(
            username=serialiser.data["username"], password=serialiser.data["password"]
        )
        if not user:
            return Response(
                {"status": "error", "message": "invalid credential"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"status": "success", "message": "login sucess", "token": str(token)},
            status=status.HTTP_200_OK,
        )
