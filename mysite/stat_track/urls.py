from django .urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("moderator", views.moderator_panel, name="moderator_panel"),
]