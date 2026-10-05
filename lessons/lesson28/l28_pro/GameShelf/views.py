from django.shortcuts import get_object_or_404, render

from .forms import CatalogFilterForm
from .models import Game


def home(request):
    return render(request, "home.html")


def game_list(request):
    games = Game.objects.select_related("studio").order_by("title", "pk")
    filter_form = CatalogFilterForm(request.GET)
    if filter_form.is_valid():
        genre = filter_form.cleaned_data["genre"]
        if genre:
            games = games.filter(genres=genre)
    else:
        games = games.none()
    return render(request, "game_list.html", {"games": games, "filter_form": filter_form})


def game_detail(request, pk):
    game = get_object_or_404(
        Game.objects.select_related("studio").prefetch_related("genres"), pk=pk
    )
    return render(request, "game_detail.html", {"game": game})
