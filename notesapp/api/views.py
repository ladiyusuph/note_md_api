from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from notesapp.models import Note
from .serializers import NoteSerializer
import language_tool_python
from rest_framework.exceptions import NotFound


class NoteView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = NoteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if request.user.is_authenticated:
            user = request.user
        else:
            return Response({"error": "Authentication required"})
        # user = get_object_or_404(User, pk=request.user.pk)
        if serializer.is_valid():
            # you can access the file like this from serializer
            # uploaded_file = serializer.validated_data["file"]
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
        else:
            return Response({"error": "Authentication required"})
        notes = Note.objects.filter(owner=request.user)
        serializer = self.serializer_class(notes, many=True)

        return Response(serializer.data)


# class GrammarCheck(GenericAPIView):
#     serializer_class = NoteSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         notes = Note.objects.filter(owner=self.request.user)
#         return notes

#     def get(self, request, *args, **kwargs):
#         try:
#             note = self.get_object()
#         except Note.DoesNotExist:
#             raise NotFound("Note not found")

#         # Open the file associated with the note and check grammar
#         file_path = note.file.path
#         with open(file_path, "r") as file:
#             content = file.read()
#             grammar_check_result = self.check_grammar(content)

#         serializer = self.serializer_class(note)
#         return Response(
#             {"serializer": serializer.data, "grammar_check": grammar_check_result}
#         )

#     def check_grammar(self, text):
#         tool = language_tool_python.LanguageTool("en-US")
#         matches = tool.check(text)
#         return [match.message for match in matches]
