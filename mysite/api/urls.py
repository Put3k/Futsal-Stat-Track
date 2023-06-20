from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.api_home),
    path('players/', views.player_list_create_view),
    path('players/<int:pk>/', views.player_detail_view),
]