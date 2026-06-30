import requests
import datetime
from django.conf import settings
from .models import Game

# Generates the igdb token to link the database
def get_igdb_token(): 
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        'client_id': settings.IGDB_CLIENT_ID,
        'client_secret': settings.IGDB_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    responce = requests.post(url, params=params)
    return responce.json()['access_token']

# Runs the commands to update the game models with database information
def fetch_game_from_igdb(title):
    token = get_igdb_token()
    headers = {
        'Client-ID': settings.IGDB_CLIENT_ID,
        'Authorization': f'Bearer {token}'
    }
    body = f'search "{title}"; fields name,cover.url,first_release_date,platforms.name,involved_companies.company.name,involved_companies.company.start_date,involved_companies.company.country,involved_companies.developer; limit 5;'
    response = requests.post(
        'https://api.igdb.com/v4/games',
        headers = headers,
        data = body
    )
    return response.json()

# saves the results to the proper model
import datetime
from .models import Game, Developer

def save_igdb_results(results):
    for entry in results:
        developer_obj = None

        for company in entry.get('involved_companies', []):
            if company.get('developer'):
                company_data = company['company']
                developer_obj, _ = Developer.objects.update_or_create(
                    name=company_data['name'],
                    defaults={
                        'date_established': (
                            datetime.date.fromtimestamp(company_data['start_date'])
                            if company_data.get('start_date') else None
                        ),
                        'location': str(company_data.get('country', '')) if company_data.get('country') else '',
                    }
                )
                break  # take the first listed developer only

        Game.objects.update_or_create(
            igdb_id=entry['id'],
            defaults={
                'title': entry['name'],
                'cover_image_url': 'https:' + entry['cover']['url'] if entry.get('cover') else '',
                'release_date': datetime.date.fromtimestamp(entry['first_release_date']) if entry.get('first_release_date') else None,
                'developer': developer_obj,
            }
        )