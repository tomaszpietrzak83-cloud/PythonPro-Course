from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


# TASK 10
@cache_page(60)
@api_view(["GET"])
def product_list(request):
    products = Product.objects.all().order_by("id")
    serializer = ProductSerializer(products, many=True)
    return Response(
        {
            "cache_backend": "Redis",
            "count": len(serializer.data),
            "products": serializer.data,
        }
    )


# Extra DRF endpoint for checking cache with a ViewSet.
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
