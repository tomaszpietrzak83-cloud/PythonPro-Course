from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Note, Product
from .serializers import NoteSerializer, ProductSerializer


# TASK 03
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# TASK 06
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by("-created_at")
    serializer_class = NoteSerializer


@api_view(["GET"])
# TASK 05
def set_name(request):
    name = request.GET.get("name")

    if not name:
        return Response({"error": "Enter name."}, status=400)

    response = Response({"message": f"Name set: {name}"})
    response.set_cookie("user_name", name, max_age=3600)
    return response


@api_view(["GET"])
# TASK 05
def hello(request):
    name = request.COOKIES.get("user_name", "Guest")
    return Response({"message": f"Hello, {name}!"})
