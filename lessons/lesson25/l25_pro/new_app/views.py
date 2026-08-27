from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


# TASK 03
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
