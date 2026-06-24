from django.contrib import admin
from games.models import Game, Review, Profile, TopGames

admin.site.register(Game)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(TopGames)