# Lekcja 27: Cache w Django REST Framework

`#lekcja` `#python` `#django` `#drf` `#cache` `#performance` `#optymalizacja`

W tej lekcji dowiemy się, czym jest mechanizm cache, czyli pamięci podręcznej, i jak używać go w Django oraz Django REST Framework.

Cache pozwala przyspieszyć aplikację, odciążyć bazę danych i skrócić czas odpowiedzi serwera.

## 1. Czym jest cache?

Każde żądanie do aplikacji, które wymaga odpytania bazy danych, kosztuje czas i zasoby.

Jeśli dane nie zmieniają się często, nie zawsze warto pobierać je od nowa z bazy. Możemy pobrać je raz, zapisać w szybkim magazynie i przy kolejnych żądaniach zwracać właśnie z tego magazynu.

> [!definition]
>
> Cache, czyli pamięć podręczna, to mechanizm przechowywania danych w tymczasowym, szybkim magazynie. Dzięki temu przyszłe żądania dotyczące tych samych danych mogą być obsłużone szybciej.

Podstawowe pojęcia:

- **Cache miss** - danych nie ma w cache, więc aplikacja musi pobrać je z bazy albo policzyć od nowa.
- **Cache hit** - dane są w cache, więc aplikacja może zwrócić je szybciej.

Schemat bez cache:

```text
Klient -> Aplikacja Django -> Baza danych -> Aplikacja Django -> Klient
```

Schemat z cache:

```text
Klient -> Aplikacja Django -> Sprawdź cache
                             -> cache hit: zwróć dane z cache
                             -> cache miss: pobierz z bazy i zapisz w cache
```

<p style="color:red"><strong>Komentarz mentora:</strong> Cache nie jest miejscem na dane, które muszą być zawsze idealnie aktualne. To kompromis między szybkością a świeżością danych.</p>

## 2. Konfiguracja cache w `settings.py`

Django oferuje kilka backendów cache. Konfigurujemy je w słowniku `CACHES` w pliku `settings.py`.

### Cache w pamięci

To najprostszy typ cache. Każdy proces Pythona ma swoją prywatną instancję cache.

> [!info]
>
> Django domyślnie może używać lokalnej pamięci podręcznej dla każdego procesu. Jest szybka, ale nie jest współdzielona między procesami serwera. Nadaje się głównie do developmentu.

```python
# settings.py

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
```

### Cache oparty na systemie plików

Django może przechowywać zbuforowane dane w plikach na serwerze.

```python
# settings.py

import os

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "django_cache"),
    }
}
```

### Cache w bazie danych

Można używać bazy danych jako magazynu cache, ale to najwolniejsza z opcji i rzadko jest zalecana.

```python
# settings.py

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "my_cache_table",
    }
}
```

Przed użyciem cache w bazie danych trzeba utworzyć tabelę:

```bash
python manage.py createcachetable
```

> [!tip]
>
> W środowiskach produkcyjnych najczęściej używa się zewnętrznych systemów cache, takich jak Redis albo Memcached.

## 3. Cache na poziomie widoku

Najprostszym sposobem dodania cache do widoku jest dekorator `@cache_page`.

> [!definition]
>
> `@cache_page(timeout)` przyjmuje czas w sekundach. Określa on, jak długo odpowiedź widoku ma być przechowywana w cache.

Przykład widoku funkcyjnego DRF:

```python
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product


@cache_page(60 * 15)  # cache na 15 minut
@api_view(["GET"])
def product_list(request):
    products = Product.objects.all()
    data = {"products": list(products.values())}
    return Response(data)
```

Ta część kodu wykona się tylko wtedy, gdy odpowiedzi nie ma jeszcze w cache.

## 4. Cache w widokach klasowych i ViewSetach

Dla widoków opartych na klasach albo ViewSetów z DRF można użyć `method_decorator`.

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

Ten przykład cachuje metodę `list`, czyli najczęściej request `GET /products/`.

<p style="color:red"><strong>Komentarz mentora:</strong> Uważaj z cachowaniem endpointów, które zależą od zalogowanego użytkownika. Źle dobrany cache może zwrócić dane jednego użytkownika innemu.</p>

## 5. Niskopoziomowe API cache

Django udostępnia też API do ręcznego zarządzania cache. Daje ono większą kontrolę nad tym, co i kiedy zapisujemy.

To podejście przydaje się szczególnie do cachowania kosztownych obliczeń, a nie całych odpowiedzi HTTP.

```python
# services.py

import time

from django.core.cache import cache


def get_very_complex_calculation_result():
    cache_key = "complex_calculation"

    result = cache.get(cache_key)

    if result is None:
        print("Wykonuję skomplikowane obliczenia...")
        time.sleep(5)

        result = {"data": 42, "source": "Obliczone na żywo"}
        cache.set(cache_key, result, timeout=3600)
    else:
        print("Zwracam wynik z cache!")
        result["source"] = "Pobrane z cache"

    return result
```

Przykład użycia w widoku:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import get_very_complex_calculation_result


@api_view(["GET"])
def complex_view(request):
    data = get_very_complex_calculation_result()
    return Response(data)
```

## 6. Django Debug Toolbar

Skąd wiedzieć, czy cache działa poprawnie? Pomaga w tym `django-debug-toolbar`.

> [!info]
>
> Django Debug Toolbar to panel wyświetlany na stronie podczas developmentu. Pokazuje informacje o bieżącym żądaniu i odpowiedzi, między innymi zapytania do bazy danych, szablony, ustawienia oraz operacje na cache.

Instalacja:

```bash
pip install django-debug-toolbar
```

Dodanie do `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "django.contrib.staticfiles",
    "debug_toolbar",
]
```

Dodanie middleware:

```python
MIDDLEWARE = [
    # ...
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # ...
]
```

Konfiguracja `INTERNAL_IPS`:

```python
INTERNAL_IPS = [
    "127.0.0.1",
]
```

Dodanie URL-i:

```python
from django.urls import include, path

urlpatterns = [
    # ...
    path("__debug__/", include("debug_toolbar.urls")),
]
```

Po odświeżeniu strony w aplikacji powinien pojawić się panel. W zakładce `Cache` można zobaczyć operacje cache, czas ich trwania oraz informację, czy był to `hit`, czy `miss`.

## 7. Cache invalidation

Jednym z największych wyzwań w cachingu jest unieważnianie cache, czyli decyzja, kiedy usunąć stare dane.

Przykład problemu:

1. Użytkownik pobiera listę produktów.
2. Lista zapisuje się w cache na 15 minut.
3. Administrator zmienia cenę produktu.
4. Przez kilka minut użytkownicy mogą nadal widzieć starą cenę.

Dlatego przy cache trzeba myśleć nie tylko o zapisaniu danych, ale też o ich usuwaniu lub odświeżaniu.

<p style="color:red"><strong>Komentarz mentora:</strong> Najtrudniejsza część cache to zwykle nie samo `cache.set()`, tylko dobra odpowiedź na pytanie: kiedy dane przestają być aktualne?</p>

## 8. Podsumowanie

W tej lekcji nauczyliśmy się:

- czym jest cache,
- czym różni się cache hit od cache miss,
- jak skonfigurować `LocMemCache`, `FileBasedCache` i `DatabaseCache`,
- jak używać dekoratora `@cache_page`,
- jak używać cache w ViewSetach przez `method_decorator`,
- jak korzystać z niskopoziomowego API `django.core.cache.cache`,
- jak sprawdzać działanie cache przez Django Debug Toolbar,
- dlaczego unieważnianie cache jest ważne.
