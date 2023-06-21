from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.api_home),
    path('auth/', obtain_auth_token),
    path('players/', views.player_list_create_view),
    path('players/<int:pk>/update/', views.player_update_view),
    path('players/<int:pk>/delete/', views.player_delete_view),
    path('players/<int:pk>/', views.player_detail_view),
]