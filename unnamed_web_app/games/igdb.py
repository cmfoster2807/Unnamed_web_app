# games/igdb.py

import requests
from django.conf import settings

# ── Auth ──────────────────────────────────────────────────────────────────────

def get_access_token():
    """Exchange client credentials for a Twitch/IGDB access token."""
    response = requests.post(
        'https://id.twitch.tv/oauth2/token',
        params={
            'client_id': settings.IGDB_CLIENT_ID,
            'client_secret': settings.IGDB_CLIENT_SECRET,
            'grant_type': 'client_credentials',
        }
    )
    response.raise_for_status()
    return response.json()['access_token']


def get_headers():
    """Return headers required for every IGDB request."""
    return {
        'Client-ID': settings.IGDB_CLIENT_ID,
        'Authorization': f'Bearer {get_access_token()}',
    }


# ── Search ────────────────────────────────────────────────────────────────────

def search_games(query):
    """Search IGDB for games by name."""
    response = requests.post(
        'https://api.igdb.com/v4/games',
        headers=get_headers(),
        data=f'''
            fields name, cover.url, first_release_date, 
                   genres.name, platforms.name, summary,
                   involved_companies.company.name,
                   involved_companies.developer;
            search "{query}";
            limit 10;
        '''
    )
    return response.json()

def search_developers(query):
    """Search IGDB for companies (developers/publishers) by name."""
    response = requests.post(
        'https://api.igdb.com/v4/companies',
        headers=get_headers(),
        data=f'''
            fields name, logo.url, description;
            search "{query}";
            limit 10;
        '''
    )
    return response.json()


def get_games_by_developer(company_id):
    """Fetch games where this company is a developer."""
    response = requests.post(
        'https://api.igdb.com/v4/games',
        headers=get_headers(),
        data=f'''
            fields name, cover.url, first_release_date, genres.name;
            where involved_companies.company = {company_id} 
                  & involved_companies.developer = true;
            limit 50;
        '''
    )
    return response.json()

# ── Fetch single game ─────────────────────────────────────────────────────────

def get_game(igdb_id):
    """Fetch a single game by IGDB ID."""
    response = requests.post(
        'https://api.igdb.com/v4/games',
        headers=get_headers(),
        data=f'''
            fields name, cover.url, first_release_date,
                   genres.name, platforms.name, summary,
                   involved_companies.company.name,
                   involved_companies.developer;
            where id = {igdb_id};
        '''
    )
    data = response.json()
    return data[0] if data else None


# ── Sync to database ──────────────────────────────────────────────────────────

def sync_game(igdb_id):
    """Fetch a game from IGDB and save it to the local database."""
    from .models import Game, Developer
    import datetime

    data = get_game(igdb_id)
    if not data:
        return None

    # Handle cover image URL
    cover_url = ''
    if 'cover' in data:
        cover_url = 'https:' + data['cover']['url'].replace('t_thumb', 't_cover_big')

    # Handle release date (IGDB sends it as a Unix timestamp)
    release_date = None
    if 'first_release_date' in data:
        release_date = datetime.date.fromtimestamp(data['first_release_date'])

    # Handle platforms
    platforms = ', '.join(p['name'] for p in data.get('platforms', []))

    # Handle genres
    genres = ', '.join(g['name'] for g in data.get('genres', []))

    # Create or update the game
    game, created = Game.objects.update_or_create(
        igdb_id=igdb_id,
        defaults={
            'title': data['name'],
            'cover_image_url': cover_url,
            'release_date': release_date,
            'platform': platforms,
            'genre': genres,
            'description': data.get('summary', ''),
        }
    )

    # Handle developers
    for company in data.get('involved_companies', []):
        if company.get('developer'):
            dev, _ = Developer.objects.get_or_create(
                name=company['company']['name'],
                defaults={
                    'igdb_id': company['company'].get('id'),
                }
            )
            game.developers.add(dev)

    return game

def sync_developer(igdb_company_id):
    """Fetch a developer's games from IGDB and sync them locally."""
    from .models import Developer, Game

    games_data = get_games_by_developer(igdb_company_id)
    if not games_data:
        return None

    developer = None
    for g in games_data:
        game = sync_game(g['id'])  # reuses your existing sync_game function
        if game:
            for dev in game.developers.filter(igdb_id=igdb_company_id):
                developer = dev

    return developer
