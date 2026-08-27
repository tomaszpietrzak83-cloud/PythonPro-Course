from rest_framework import serializers

from .models import Author, Book, Note, Product


# TASK 09
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


# TASK 09
class BookSerializer(serializers.ModelSerializer):
    # TASK 09
    author_name = serializers.StringRelatedField(
        source="author", read_only=True
    )

    class Meta:
        model = Book
        fields = ("id", "title", "publication_year", "author", "author_name")


# TASK 06
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"


# TASK 02
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
