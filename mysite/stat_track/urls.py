from django .urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("moderator", views.moderator_panel, name="moderator_panel"),
    path('player/<int:player_id>/', views.player_stats, name="player_stats"),
    path('match/<int:match_id>/', views.match_stats, name="match_stats"),
]