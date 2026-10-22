from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .forms import CatalogFilterForm, LibraryFilterForm, UserGameEditForm
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


@login_required
@require_POST
def add_to_wishlist(request, pk):
    game = get_object_or_404(Game, pk=pk)
    entry, _ = UserGame.objects.get_or_create(
        user=request.user, game=game, defaults={"list_type": UserGame.ListType.WISHLIST}
    )
    if entry.list_type == UserGame.ListType.OWNED:
        messages.info(request, "This game is already owned. It stays in your owned games.")
    else:
        messages.success(request, f"{game.title} is now on your wishlist.")
    return redirect("gameshelf:game_detail", pk=game.pk)


@login_required
@require_GET
def my_library(request):
    entries = UserGame.objects.filter(user=request.user).select_related(
        "game", "game__studio"
    ).order_by("game__title", "pk")
    library_form = LibraryFilterForm(request.GET)
    if library_form.is_valid():
        list_type = library_form.cleaned_data["list_type"]
        if list_type and list_type != "all":
            entries = entries.filter(list_type=list_type)
    else:
        entries = entries.none()
    return render(
        request, "my_library.html", {"entries": entries, "library_form": library_form}
    )


@login_required
@require_http_methods(["GET", "POST"])
def edit_library_entry(request, pk):
    entry = get_object_or_404(
        UserGame.objects.select_related("game"), pk=pk, user=request.user
    )
    form = UserGameEditForm(
        request.POST if request.method == "POST" else None, instance=entry
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Your entry for {entry.game.title} has been updated.")
        return redirect("gameshelf:my_library")
    return render(request, "edit_library_entry.html", {"entry": entry, "form": form})


@login_required
@require_http_methods(["GET", "POST"])
def remove_library_entry(request, pk):
    entry = get_object_or_404(
        UserGame.objects.select_related("game"), pk=pk, user=request.user
    )
    if request.method == "POST":
        title = entry.game.title
        entry.delete()
        messages.success(request, f"{title} has been removed from your library.")
        return redirect("gameshelf:my_library")
    return render(request, "remove_library_entry.html", {"entry": entry})
