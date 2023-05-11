from django .urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("moderator", views.moderator_panel, name="moderator_panel"),
    path('player/<int:player_id>/', views.player_stats, name="player_stats"),
    path('matchday/<int:matchday_id>/', views.matchday, name="matchday"),
    path('create_matchday/', views.match_creator_matchday, name="create_matchday"),
    path('matchday/<int:matchday_id>/edit', views.edit_matchday, name="edit_matchday"),
    path('delete_match/<int:match_id>/', views.delete_match, name="delete_match"),
    path('add_player', views.add_player, name="add_player"),
    
    path('ajax_load_players/', views.load_players, name='ajax_load_players'), #AJAX
]