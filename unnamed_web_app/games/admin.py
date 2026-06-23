from django.contrib import admin
from ..unnamed_web_app.models import Game, Review, Profile, TopGames

admin.site.register(Game)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(TopGames)