from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('game/<int:igdb_id>/', views.game_detail, name='game_detail'),
]