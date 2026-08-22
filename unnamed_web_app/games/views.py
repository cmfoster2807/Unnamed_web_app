from django.http import Http404
from django.shortcuts import render
from requests import RequestException

from .igdb import (
    search_developers,
    search_games,
    sync_developer,
    sync_game,
)
from .models import Developer, Game


def search(request):
    """Live search against IGDB API — games and developers."""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'games')  # toggle via query param or form field

    game_results = []
    developer_results = []
    search_error = None

    if query:
        try:
            if search_type == 'developers':
                developer_results = search_developers(query)
            else:
                game_results = search_games(query)
        except (KeyError, ValueError, RequestException):
            search_error = (
                'Game search is unavailable. Check the IGDB client ID and '
                'client secret in your local .env file.'
            )

    return render(request, 'games/search.html', {
        'game_results': game_results,
        'developer_results': developer_results,
        'query': query,
        'search_type': search_type,
        'search_error': search_error,
    })

def game_detail(request, igdb_id):
    """Serve from local DB if exists, otherwise sync from IGDB first."""
    try:
        game = Game.objects.get(igdb_id=igdb_id)
    except Game.DoesNotExist:
        game = sync_game(igdb_id)

    return render(request, 'games/game_detail.html', {'game': game})

def developer_detail(request, igdb_id):
    """Load a developer locally or synchronize it from IGDB."""

    developer = (
        Developer.objects
        .prefetch_related("games")
        .filter(igdb_id=igdb_id)
        .first()
    )

    if developer is None:
        try:
            developer = sync_developer(igdb_id)
        except (KeyError, ValueError, RequestException) as exc:
            raise Http404("Developer is unavailable.") from exc

    if developer is None:
        raise Http404("Developer not found.")

    return render(
        request,
        "games/developer_detail.html",
        {"developer": developer},
    )
