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


@api_view(["GET"])
# TASK 07
def calculate(request):
    num1 = request.GET.get("num1")
    num2 = request.GET.get("num2")
    operation = request.GET.get("operation")

    if num1 is None or num2 is None or operation is None:
        return Response({"error": "Missing required parameters."}, status=400)

    try:
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        return Response({"error": "num1 and num2 must be numbers."}, status=400)

    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return Response({"error": "Cannot divide by zero."}, status=400)
        result = num1 / num2
    else:
        return Response({"error": "Invalid operation."}, status=400)

    return Response({"result": result}, status=200)
