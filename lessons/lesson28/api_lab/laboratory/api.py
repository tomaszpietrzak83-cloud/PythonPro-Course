import re
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Product
from .serializers import (
    ProductSerializer, CategorySerializer, ErrorSerializer,
    ProductValidationErrorSerializer, CategoryQuerySerializer, QueryErrorSerializer,
    SentimentInputSerializer, SentimentOutputSerializer, TextErrorSerializer,
)


class AutomaticProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class DocstringProductList(generics.ListAPIView):
    """Pobierz katalog produktów.

    Ten widok pokazuje, jak opis klasy trafia do dokumentacji OpenAPI.
    Lista pochodzi z lokalnej bazy, a format odpowiedzi z ProductSerializer.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.order_by("id")
    serializer_class = CategorySerializer


class ProductListView(APIView):
    """Operacje na produktach: pobieranie, filtrowanie i tworzenie."""

    @extend_schema(
        summary="Pobierz produkty, opcjonalnie według kategorii", tags=["Produkty"],
        parameters=[OpenApiParameter(
            name="category", description="ID kategorii, dodatnia liczba całkowita.",
            required=False, type=OpenApiTypes.INT,
        )],
        responses={200: ProductSerializer(many=True), 400: QueryErrorSerializer},
    )
    def get(self, request):
        query = CategoryQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        products = Product.objects.all()
        if "category" in query.validated_data:
            products = products.filter(category_id=query.validated_data["category"])
        return Response(ProductSerializer(products, many=True).data)

    @extend_schema(
        summary="Dodaj produkt", tags=["Produkty"], request=ProductSerializer,
        responses={201: ProductSerializer, 400: ProductValidationErrorSerializer},
        examples=[OpenApiExample("Nowy produkt", value={"name": "Notes", "price": "19.90", "category": 1}, request_only=True)],
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    @extend_schema(
        summary="Pobierz szczegóły jednego produktu",
        description="Zwraca produkt o wskazanym ID. Nieistniejące ID daje odpowiedź 404.",
        tags=["Produkty"], responses={200: ProductSerializer, 404: ErrorSerializer},
    )
    def get(self, request, pk):
        return Response(ProductSerializer(get_object_or_404(Product, pk=pk)).data)

    @extend_schema(
        summary="Usuń produkt", tags=["Produkty"],
        responses={
            204: OpenApiResponse(description="Usunięto produkt. Odpowiedź bez treści."),
            404: OpenApiResponse(response=ErrorSerializer, description="Produkt nie istnieje."),
        },
    )
    def delete(self, request, pk):
        get_object_or_404(Product, pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SentimentView(APIView):
    @extend_schema(
        summary="Przeanalizuj wydźwięk tekstu (demonstracja regułowa)", tags=["Analiza tekstu"],
        description="Maksymalnie 500 znaków. Prosty słownik słów, bez modelu AI. Nie rozumie negacji ani ironii.",
        request=SentimentInputSerializer,
        responses={200: SentimentOutputSerializer, 400: TextErrorSerializer},
        examples=[OpenApiExample("Pozytywny tekst", value={"text": "Kocham programować w Pythonie!"}, request_only=True)],
    )
    def post(self, request):
        serializer = SentimentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data["text"]
        words = re.findall(r"\w+", text.lower())
        positive = {"kocham", "lubię", "świetny", "super", "dobry"}
        negative = {"nienawidzę", "zły", "fatalny", "okropny"}
        score = sum(word in positive for word in words) - sum(word in negative for word in words)
        return Response({
            "input_text": text,
            "sentiment": "positive" if score > 0 else "negative" if score < 0 else "neutral",
            "matched_words": [word for word in words if word in positive | negative],
            "method": "Słownik słów (demonstracja, bez modelu AI)",
        })
