from django.core.management.base import BaseCommand
from games.igdb_utils import fetch_game_from_igdb, save_igdb_results

class Command(BaseCommand):
    help = 'Fetch a game from IGDB and save it to the local database'

    def add_arguments(self, parser):
        parser.add_argument('title', type = str)

    def handle(self, *args, **options):
        results = fetch_game_from_igdb(options['title'])
        save_igdb_results(results)
        self.stdout.write(self.style.SUCCESS(f"Synced {len(results)} games"))