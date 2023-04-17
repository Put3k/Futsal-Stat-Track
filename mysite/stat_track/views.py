from django.shortcuts import render, get_object_or_404
from .models import Match, Player


def home(request):
    latest_match_list = Match.objects.order_by("-date")[:5]
    context = {"latest_match_list": latest_match_list}
    return render(request, "stat_track/home.html", context)

def moderator_panel(request):
    return HttpResponse("Moderator Panel")

def player_stats(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render(request, "stat_track/player.html", {"player": player})

def match_stats(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    return render(request, "stat_track/match.html", {"match": match})