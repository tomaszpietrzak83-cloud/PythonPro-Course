from decimal import Decimal
from rest_framework import serializers
from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=8, decimal_places=2, min_value=Decimal("0.01"))

    class Meta:
        model = Product
        fields = ["id", "name", "price", "category"]
        read_only_fields = ["id"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()


class ProductValidationErrorSerializer(serializers.Serializer):
    name = serializers.ListField(child=serializers.CharField(), required=False)
    price = serializers.ListField(child=serializers.CharField(), required=False)
    category = serializers.ListField(child=serializers.CharField(), required=False)
    non_field_errors = serializers.ListField(child=serializers.CharField(), required=False)


class CategoryQuerySerializer(serializers.Serializer):
    category = serializers.IntegerField(min_value=1, required=False)


class QueryErrorSerializer(serializers.Serializer):
    category = serializers.ListField(child=serializers.CharField())


class SentimentInputSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500, allow_blank=False)


class SentimentOutputSerializer(serializers.Serializer):
    input_text = serializers.CharField()
    sentiment = serializers.ChoiceField(choices=["positive", "negative", "neutral"])
    matched_words = serializers.ListField(child=serializers.CharField())
    method = serializers.CharField()


class TextErrorSerializer(serializers.Serializer):
    text = serializers.ListField(child=serializers.CharField(), required=False)
    non_field_errors = serializers.ListField(child=serializers.CharField(), required=False)
