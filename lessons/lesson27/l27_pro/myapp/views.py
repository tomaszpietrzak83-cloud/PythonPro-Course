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


def get_complex_product_stats(cache_backend=None, timeout=7, cache_key="task7_complex_product_stats"):
    # Optional arguments let the presentation reuse this calculation in its own cache.
    # Regular homework requests still use the original backend, key and lifetime.
    cache_backend = cache if cache_backend is None else cache_backend
    cached_stats = cache_backend.get(cache_key)

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
        "cache_time": timeout,
    }
    cache_backend.set(cache_key, stats, timeout=timeout)
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

    # These small extension points keep invalidation in the homework ViewSet.
    # A demo subclass can change storage without duplicating perform_update.
    detail_cache = cache
    detail_timeout = CLIENT_DETAIL_CACHE_TIMEOUT

    def detail_cache_key(self, client_id):
        return get_client_detail_cache_key(client_id)

    @method_decorator(cache_page(60 * 10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        client_id = kwargs.get(self.lookup_url_kwarg or self.lookup_field)
        cache_key = self.detail_cache_key(client_id)
        cached_data = self.detail_cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        self.detail_cache.set(cache_key, dict(response.data), timeout=self.detail_timeout)
        return response

    def perform_update(self, serializer):
        client = serializer.save()
        self.detail_cache.delete(self.detail_cache_key(client.id))
