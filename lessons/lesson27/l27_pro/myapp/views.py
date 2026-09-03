import time

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Client, Product
from .serializers import ClientSerializer

CLIENT_DETAIL_CACHE_TIMEOUT = 60


def get_client_detail_cache_key(client_id):
    return f"task9_client_detail:{client_id}"


# TASK 03
@cache_page(60)
@api_view(["GET"])
def product_list(request):
    products = Product.objects.all().order_by("id")
    data = []

    for product in products:
        data.append({
            "id": product.id,
            "name": product.name,
            "price": str(product.price),
            "short_description": product.short_description,
        })

    return Response({"count": len(data), "products": data})


def get_complex_product_stats():
    cache_key = "task7_complex_product_stats"
    cached_stats = cache.get(cache_key)

    if cached_stats is not None:
        cached_stats["source"] = "cache"
        return cached_stats

    time.sleep(3)

    products = Product.objects.all()
    prices = [product.price for product in products]
    total_price = sum(prices)
    product_count = len(prices)
    average_price = total_price / product_count if product_count else 0

    stats = {
        "source": "calculated",
        "total_price": str(total_price),
        "average_price": str(round(average_price, 2)),
        "most_expensive_product": products.order_by("-price").first().name
        if product_count
        else None,
        "cache_time": 7,
    }
    cache.set(cache_key, stats, timeout=7)
    return stats


# TASK 07
@api_view(["GET"])
def product_stats(request):
    simple_data = {
        "product_count": Product.objects.count(),
        "first_five_products": list(
            Product.objects.order_by("id").values_list("name", flat=True)[:5]
        ),
    }

    # Only cache the slow calculation, not the whole response.
    complex_data = get_complex_product_stats()

    return Response({
        "simple_data": simple_data,
        "complex_data": complex_data,
    })


# TASK 08
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by("id")
    serializer_class = ClientSerializer

    @method_decorator(cache_page(60 * 10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        client_id = kwargs.get(self.lookup_url_kwarg or self.lookup_field)
        cache_key = get_client_detail_cache_key(client_id)
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, dict(response.data), timeout=CLIENT_DETAIL_CACHE_TIMEOUT)
        return response

    def perform_update(self, serializer):
        client = serializer.save()
        cache.delete(get_client_detail_cache_key(client.id))
