from django.shortcuts import get_object_or_404, render

from .models import Game


def home(request):
    return render(request, "home.html")


def game_list(request):
    games = Game.objects.all()
    return render(request, "game_list.html", {"games": games})


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, "game_detail.html", {"game": game})
