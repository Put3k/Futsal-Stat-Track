from django .urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("moderator", views.moderator_panel, name="moderator_panel"),
    path('player/<int:player_id>/', views.player_stats, name="player_stats"),
    path('matchday/<int:matchday_id>/', views.matchday, name="matchday"),
    path('match_creator_matchday/', views.match_creator_matchday, name="match_creator_matchday"),
    path('match_creator_matches/', views.match_creator_matches, name="match_creator_matches"),
]