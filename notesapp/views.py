from django.shortcuts import render
from django.views.generic import DetailView
from .models import Note


class NoteRenderView(DetailView):
    model = Note

    def get(self, request, *args, **kwargs):
        note = self.get_object()
        file_path = note.file.path
        with open(file_path, "r") as file:
            content = file.read()
        # Get the title from the file path
        title = file_path.split("/")[-1] if file_path else "Unknown title"
        context = {"note": note, "title": title, "content": content}
        return render(request, "note.html", context=context)
