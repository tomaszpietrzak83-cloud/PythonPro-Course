from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("notes/", views.notes_list, name="notes_list"),
    path("note/<int:note_id>/", views.note_detail, name="note_detail"),
]
