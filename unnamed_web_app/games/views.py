from django.shortcuts import render, get_object_or_404
from .models import Game
from .igdb import search_games, sync_game


def search(request):
    """Live search against IGDB API."""
    query = request.GET.get('q', '')
    results = []
    if query:
        results = search_games(query)
    return render(request, 'games/search.html', {
        'results': results,
        'query': query,
    })


def game_detail(request, igdb_id):
    """Serve from local DB if exists, otherwise sync from IGDB first."""
    try:
        game = Game.objects.get(igdb_id=igdb_id)
    except Game.DoesNotExist:
        game = sync_game(igdb_id)

    return render(request, 'games/game_detail.html', {'game': game})