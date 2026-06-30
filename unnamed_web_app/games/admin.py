from django.contrib import admin
from games.models import Game, Review, Profile, TopGames, GameList, GameListEntry, Developer

admin.site.register(Game)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(TopGames)
admin.site.register(GameList)
admin.site.register(GameListEntry)
admin.site.register(Developer)