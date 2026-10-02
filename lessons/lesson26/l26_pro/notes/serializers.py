from rest_framework import serializers

from .models import Note


# TASK 25
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at"]
        read_only_fields = ["id", "created_at"]
