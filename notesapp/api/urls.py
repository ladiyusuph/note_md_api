from django.urls import path
from . import views

urlpatterns = [
    path("", views.NoteView.as_view(), name="upload-note"),
    # path("grammar/<int:pk>", views.GrammarCheck.as_view(), name="check-grammer"),
]
