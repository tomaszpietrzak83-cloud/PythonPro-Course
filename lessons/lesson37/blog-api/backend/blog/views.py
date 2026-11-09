from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        # Sprawdź cache
        cache_key = "posts_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response({"source": "cache", "data": cached_data})

        # Jeśli nie ma w cache, pobierz z bazy
        queryset = self.get_queryset().filter(published=True)
        serializer = self.get_serializer(queryset, many=True)

        # Zapisz do cache na 5 minut
        cache.set(cache_key, serializer.data, 300)

        return Response({"source": "database", "data": serializer.data})

    @action(detail=False, methods=["post"])
    def clear_cache(self, request):
        cache.clear()
        return Response({"message": "Cache cleared"})


print("Django aplikacja z PostgreSQL i Redis cache")
