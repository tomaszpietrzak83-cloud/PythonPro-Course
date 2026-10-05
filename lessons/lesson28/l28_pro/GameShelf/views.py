from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .forms import CatalogFilterForm
from .models import Game


def home(request):
    return render(request, "home.html")


def filtered_games(params):
    """Share search and filter rules between the catalog and live suggestions."""
    games = Game.objects.select_related("studio").order_by("title", "pk")
    filter_form = CatalogFilterForm(params)
    if filter_form.is_valid():
        query = filter_form.cleaned_data["q"]
        if query:
            games = games.filter(title__icontains=query)
        genre = filter_form.cleaned_data["genre"]
        if genre:
            games = games.filter(genres=genre)
        tag = filter_form.cleaned_data["tag"]
        if tag:
            games = games.filter(tags=tag)
    else:
        games = games.none()
    return games, filter_form


def game_list(request):
    games, filter_form = filtered_games(request.GET)
    return render(
        request, "game_list.html", {"games": games, "filter_form": filter_form}
    )


@require_GET
def game_suggestions(request):
    games, filter_form = filtered_games(request.GET)
    if not filter_form.is_valid() or not filter_form.cleaned_data["q"]:
        return JsonResponse({"results": []})
    results = [
        {"title": game.title, "url": reverse("gameshelf:game_detail", args=[game.pk])}
        for game in games[:3]
    ]
    return JsonResponse({"results": results})


def game_detail(request, pk):
    game = get_object_or_404(
        Game.objects.select_related("studio").prefetch_related("genres", "tags"), pk=pk
    )
    return render(request, "game_detail.html", {"game": game})
