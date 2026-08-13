from django.shortcuts import render, get_object_or_404
from .models import Game
from .igdb import search_games, sync_game


def search(request):
    """Live search against IGDB API — games and developers."""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'games')  # toggle via query param or form field

    game_results = []
    developer_results = []

    if query:
        if search_type == 'developers':
            developer_results = search_developers(query)
        else:
            game_results = search_games(query)

    return render(request, 'games/search.html', {
        'game_results': game_results,
        'developer_results': developer_results,
        'query': query,
        'search_type': search_type,
    })

def game_detail(request, igdb_id):
    """Serve from local DB if exists, otherwise sync from IGDB first."""
    try:
        game = Game.objects.get(igdb_id=igdb_id)
    except Game.DoesNotExist:
        game = sync_game(igdb_id)

    return render(request, 'games/game_detail.html', {'game': game})

def developer_detail(request, igdb_id):
    """Serve from local DB if exists, otherwise sync from IGDB first."""
    from .models import Developer
    from .igdb import sync_developer

    try:
        developer = Developer.objects.get(igdb_id=igdb_id)
    except Developer.DoesNotExist:
        developer = sync_developer(igdb_id)

    return render(request, 'games/developer_detail.html', {'developer': developer})