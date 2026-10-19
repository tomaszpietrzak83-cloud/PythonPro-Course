from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .forms import CatalogFilterForm
from .models import Game, UserGame


def home(request):
    return render(request, "home.html")


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("gameshelf:game_list")
    form = UserCreationForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your account is ready. You can now log in.")
        return redirect("gameshelf:login")
    return render(request, "registration/register.html", {"form": form})


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
    library_entry = None
    if request.user.is_authenticated:
        library_entry = UserGame.objects.filter(user=request.user, game=game).first()
    return render(
        request, "game_detail.html", {"game": game, "library_entry": library_entry}
    )


@login_required
@require_POST
def add_to_owned(request, pk):
    game = get_object_or_404(Game, pk=pk)
    UserGame.objects.update_or_create(
        user=request.user, game=game, defaults={"list_type": UserGame.ListType.OWNED}
    )
    messages.success(request, f"{game.title} is now in your owned games.")
    return redirect("gameshelf:game_detail", pk=game.pk)
