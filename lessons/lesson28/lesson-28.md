# Lekcja 28: Dokumentacja API w Django REST Framework

`#lekcja` `#python` `#django` `#drf` `#api` `#openapi` `#swagger` `#documentation`

## 1. Dlaczego dokumentacja API jest ważna?

Wyobraź sobie, że budujesz skomplikowaną maszynę, ale nie tworzysz do niej żadnej instrukcji obsługi. Tylko Ty wiesz, jak jej używać. Każda nowa osoba, która będzie chciała z niej skorzystać, będzie musiała zgadywać albo ciągle pytać Cię o pomoc.

Podobnie jest z API.

Dobra dokumentacja API jest jak czytelna instrukcja obsługi. Dzięki niej:

- frontend deweloperzy wiedzą, jakich endpointów używać, jakie dane wysyłać i co otrzymają w odpowiedzi,
- nowi członkowie zespołu mogą szybko zrozumieć backend,
- użytkownicy zewnętrzni mogą łatwiej integrować swoje aplikacje z systemem,
- Ty sam po kilku miesiącach możesz szybciej wrócić do projektu.

> [!info]
>
> API, czyli Interfejs Programowania Aplikacji, to "kontrakt" między serwerem a klientem. Określa, jak obie strony mają się komunikować: jakie dane można wysłać, w jakim formacie i jakiej odpowiedzi można się spodziewać.

<p style="color:red"><strong>Komentarz mentora:</strong> Dobra dokumentacja API nie jest dodatkiem na koniec. Najlepiej aktualizować ją razem ze zmianami w endpointach.</p>

## 2. OpenAPI i Swagger

Kiedy mówimy o dokumentacji API, często pojawiają się dwa terminy: **OpenAPI** i **Swagger**.

Ważne jest rozróżnienie:

- **OpenAPI** to standard opisu API.
- **Swagger** to zestaw narzędzi, które pracują ze specyfikacją OpenAPI.

> [!definition]
>
> OpenAPI Specification to standard, który definiuje, jak opisywać API REST. Jest to plik w formacie JSON lub YAML, zawierający informacje o endpointach, metodach HTTP, parametrach, formatach danych i możliwych odpowiedziach.

> [!definition]
>
> Swagger to zestaw narzędzi zbudowanych wokół specyfikacji OpenAPI.

Najpopularniejsze narzędzia Swagger:

- **Swagger UI** - generuje interaktywną dokumentację API w przeglądarce.
- **Swagger Editor** - edytor do tworzenia i walidacji specyfikacji OpenAPI.
- **Swagger Codegen** - narzędzie do generowania kodu klienta lub szkieletu serwera na podstawie specyfikacji.

Podsumowanie:

```text
OpenAPI = standard / specyfikacja
Swagger = narzędzia używające OpenAPI
```

## 3. Integracja Swagger UI z Django REST Framework

Ręczne pisanie specyfikacji OpenAPI byłoby czasochłonne.

W Django REST Framework możemy użyć biblioteki `drf-spectacular`, która analizuje widoki, serializery i routing, a potem automatycznie generuje dokumentację API.

### Krok 1: Instalacja

```bash
pip install drf-spectacular
```

### Krok 2: Konfiguracja w `settings.py`

Dodaj `drf_spectacular` do `INSTALLED_APPS`:

```python
# myproject/settings.py

INSTALLED_APPS = [
    # ... inne aplikacje
    "rest_framework",
    "drf_spectacular",
    # ...
]
```

Skonfiguruj DRF, aby używał `drf-spectacular` jako generatora schematu:

```python
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
```

Opcjonalna konfiguracja:

```python
SPECTACULAR_SETTINGS = {
    "TITLE": "Moje Wspaniałe API Projektu",
    "DESCRIPTION": "Dokumentacja dla API, które robi niesamowite rzeczy.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
```

### Krok 3: Dodanie URL-i dokumentacji

W głównym pliku `urls.py` dodaj ścieżki do schematu, Swagger UI i ReDoc.

```python
# myproject/urls.py

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("myapp.urls")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
```

Po uruchomieniu serwera:

```bash
python manage.py runserver
```

Dokumentacja Swagger UI będzie dostępna pod adresem:

```text
http://127.0.0.1:8000/api/schema/swagger-ui/
```

## 4. Ulepszanie automatycznie generowanej dokumentacji

`drf-spectacular` dobrze analizuje serializery i widoki, ale czasem warto dodać więcej szczegółów ręcznie.

Możemy używać:

- docstringów,
- dekoratora `@extend_schema`,
- parametrów `OpenApiParameter`,
- odpowiedzi `OpenApiResponse`.

## 5. Użycie docstringów

Biblioteka może pobierać opisy z docstringów klas widoków, na przykład `APIView` albo `ViewSet`.

```python
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


class ProductListView(APIView):
    """
    Ten widok obsługuje operacje na liście produktów.

    * Pozwala na pobranie listy wszystkich produktów.
    * Pozwala na dodanie nowego produktu.
    """

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass
```

## 6. Dekorator `@extend_schema`

`@extend_schema` pozwala doprecyzować dokumentację pojedynczego endpointu.

Import:

```python
from drf_spectacular.utils import extend_schema
```

Możemy go używać nad metodami w widokach klasowych, na przykład `get`, `post`, `delete`, albo nad widokami funkcyjnymi.

### Przykład 1: Podsumowanie, opis i tagi

```python
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView


class ProductDetailView(APIView):
    @extend_schema(
        summary="Pobierz szczegóły jednego produktu",
        description="Zwraca pełne informacje o produkcie na podstawie jego ID.",
        tags=["Produkty"],
    )
    def get(self, request, pk):
        pass
```

### Przykład 2: Parametry zapytania

```python
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.views import APIView


class ProductListView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="category",
                description="Filtruj produkty po ID kategorii",
                required=False,
                type=OpenApiTypes.INT,
            ),
        ],
        tags=["Produkty"],
    )
    def get(self, request):
        category_id = request.query_params.get("category")
        pass
```

### Przykład 3: Różne kody odpowiedzi

```python
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.views import APIView

from .serializers import ErrorSerializer


class ProductDetailView(APIView):
    @extend_schema(
        summary="Usuń produkt",
        tags=["Produkty"],
        responses={
            204: OpenApiResponse(
                description="Produkt został pomyślnie usunięty (brak zawartości)"
            ),
            404: OpenApiResponse(
                description="Nie znaleziono produktu o podanym ID",
                response=ErrorSerializer,
            ),
        },
    )
    def delete(self, request, pk):
        pass
```

<p style="color:red"><strong>Komentarz mentora:</strong> Gdy używasz `pass` w przykładach lekcyjnych, pamiętaj, że to tylko placeholder. W prawdziwym widoku musi pojawić się konkretna logika albo zwrócenie odpowiedzi.</p>

## 7. Wzmianka o AI w kontekście API

API nie musi ograniczać się tylko do operacji CRUD na bazie danych. Może być też bramą do bardziej zaawansowanych funkcji, na przykład modeli sztucznej inteligencji.

Przykład: API do analizy sentymentu tekstu.

Klient wysyła tekst:

```json
{
  "text": "Kocham programować w Pythonie!"
}
```

Serwer analizuje go i zwraca wynik:

```json
{
  "input_text": "Kocham programować w Pythonie!",
  "sentiment": "positive",
  "confidence_score": 0.98
}
```

W takiej dokumentacji trzeba jasno opisać:

- format wejściowy,
- format wyjściowy,
- ograniczenia, na przykład maksymalną długość tekstu,
- możliwe błędy, na przykład pusty tekst.

Dzięki `drf-spectacular` można to opisać w dokumentacji API tak, aby endpoint był łatwy do użycia dla innych osób.

## 8. Podsumowanie

W tej lekcji pojawiły się najważniejsze elementy dokumentacji API:

- API jako kontrakt między backendem a klientem,
- OpenAPI jako standard opisu REST API,
- Swagger jako zestaw narzędzi korzystających z OpenAPI,
- `drf-spectacular` jako biblioteka do generowania dokumentacji w DRF,
- Swagger UI i ReDoc jako widoki dokumentacji,
- docstringi i `@extend_schema` jako sposoby ulepszania dokumentacji,
- potrzeba dokładnego dokumentowania endpointów, szczególnie gdy API obsługuje bardziej zaawansowane funkcje.
