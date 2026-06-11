from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Note

# --- TASK 06 ---
# def notes_list(request):
#     notes = Note.objects.all()
#     return render(request, "note_list.html", {"notes": notes})


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, "note_detail.html", {"note": note})


# --- TASK 10 ---
def notes_list(request):
    notes = Note.objects.all().order_by("id")
    paginator = Paginator(notes, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "note_list.html", {"page_obj": page_obj})
