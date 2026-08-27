from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('game/<int:igdb_id>/', views.game_detail, name='game_detail'),
    path('developers/<int:igdb_id>/', views.developer_detail, name='developer_detail'),
    path('users/<str:username>/', views.profile_detail, name='profile_detail'),
    path('users/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
]