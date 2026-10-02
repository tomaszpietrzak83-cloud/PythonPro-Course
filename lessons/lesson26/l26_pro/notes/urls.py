from django.urls import path

from .views import MyNoteDetailView, MyNotesView

# TASK 25
urlpatterns = [
    path("notes/", MyNotesView.as_view(), name="my-notes"),
    path("notes/<int:pk>/", MyNoteDetailView.as_view(), name="my-note-detail"),
]
