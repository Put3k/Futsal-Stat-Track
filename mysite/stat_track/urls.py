from django .urls import path
from . import views


urlpatterns = [
    #HTML Views
    path("", views.home, name="home"),
    path("moderator", views.moderator_panel, name="moderator_panel"), #not in use
    path('player/<int:player_id>/', views.player_stats, name="player_stats"),
    path('players_list/', views.players_list, name="players_list" ),
    path('matchday/<int:matchday_id>/', views.matchday, name="matchday"),
    path('create_matchday/', views.match_creator_matchday, name="create_matchday"),
    path('matchday/<int:matchday_id>/edit', views.edit_matchday, name="edit_matchday"),
    path('delete_match/<int:match_id>/', views.delete_match, name="delete_match"),
    
    #AJAX Data Views
    path('ajax_load_players/', views.load_players, name='ajax_load_players'), #AJAX

    #API View
    path('<int:pk>/', views.PlayerDetailAPIView.as_view())
]