from django.urls import path, include
from . import views

urlpatterns = [
    path("api/v1/", include("notesapp.api.urls")),
    path("<int:pk>", views.NoteRenderView.as_view(), name="render-note"),
]
