# from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# TASK 08
class SomeProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_name = request.user.username
        return Response({"user_name": user_name}, status=200)


# TASK 18
class AdminInfoView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"message": "Witaj w sekcji administratora."})


# TASK 25
class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        user_model = get_user_model()
        return Response({"users_count": user_model.objects.count()})


# TASK 22
class RequestIdView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"request_id": request.request_id})


# TASK 25
class StatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


# TASK 24
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
