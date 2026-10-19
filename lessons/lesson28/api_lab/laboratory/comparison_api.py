"""Te same operacje i baza; trzy sposoby opisania identycznego API."""
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer, ProductValidationErrorSerializer, ErrorSerializer


class AutomaticProducts(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AutomaticProduct(generics.RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DocstringProducts(AutomaticProducts):
    """Katalog sklepu: oglądanie i dodawanie produktów.

    GET pokazuje produkty zapisane w sklepie.
    POST dodaje nowy produkt z nazwą, ceną i kategorią.
    Dane są wspólne dla wszystkich trzech wersji demonstracji.
    """


class DocstringProduct(AutomaticProduct):
    """Pojedynczy produkt w katalogu sklepu.

    GET pokazuje produkt o podanym numerze.
    DELETE usuwa go ze sklepu. Po usunięciu nie będzie go na liście.
    """


@extend_schema_view(
    get=extend_schema(
        summary="Obejrzyj katalog sklepu",
        description="Zwraca listę produktów. Oglądanie listy nie zmienia danych w sklepie.",
        tags=["Katalog sklepu"], responses={200: ProductSerializer(many=True)},
    ),
    post=extend_schema(
        summary="Dodaj nowy notes do sklepu",
        description="Podaj nazwę, cenę co najmniej 0,01 zł i numer istniejącej kategorii. Serwer zapisze produkt i nada mu ID. Niepoprawne dane nie zostaną zapisane.",
        tags=["Katalog sklepu"], request=ProductSerializer,
        responses={
            201: OpenApiResponse(ProductSerializer, description="Zapisano produkt. Odpowiedź zawiera jego nowy numer ID."),
            400: OpenApiResponse(ProductValidationErrorSerializer, description="Nie zapisano produktu. Popraw dane wskazane w odpowiedzi."),
        },
        examples=[OpenApiExample("Notes za 19,90 zł", value={"name": "Notes z demonstracji", "price": "19.90", "category": 1}, request_only=True)],
    ),
)
class ExtendedProducts(AutomaticProducts):
    pass


@extend_schema_view(
    get=extend_schema(
        summary="Obejrzyj jeden produkt", tags=["Katalog sklepu"],
        description="Numer w adresie wskazuje konkretny produkt.",
        responses={200: ProductSerializer, 404: ErrorSerializer},
    ),
    delete=extend_schema(
        summary="Usuń swój notes ze sklepu", tags=["Katalog sklepu"],
        description="Użyj ID zwróconego przez POST. Usunięcie dotyczy jednego produktu. Powtórne usunięcie tego samego ID daje 404.",
        responses={
            204: OpenApiResponse(description="Produkt usunięty. Odpowiedź jest pusta — to prawidłowy wynik."),
            404: OpenApiResponse(ErrorSerializer, description="Produkt o tym numerze nie istnieje lub został już usunięty."),
        },
    ),
)
class ExtendedProduct(AutomaticProduct):
    pass
