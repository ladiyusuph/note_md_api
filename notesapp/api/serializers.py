from notesapp.models import Note
from rest_framework import serializers


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["created", "updated", "file"]
        read_only_fields = ("owner",)
