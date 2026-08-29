# from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# TASK 08
class SomeProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_name = request.user.username
        return Response({"user_name": user_name}, status=200)
