from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product


# TASK 06
@cache_page(60)
@api_view(["GET"])
def product_list(request):
    products = Product.objects.all().order_by("id")
    data = []

    for product in products:
        data.append(
            {
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
                "short_description": product.short_description,
            }
        )

    return Response({"count": len(data), "products": data})
