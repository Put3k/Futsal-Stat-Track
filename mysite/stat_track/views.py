from django.shortcuts import render, redirect, get_object_or_404
from .models import MatchDay, Match, Player, Stat
from .forms import MatchDayForm
from django.db.models.functions import Lower

def home(request):
    latest_match_day_list = MatchDay.objects.order_by("-date")[:5]
    players_list = Player.objects.all().order_by("last_name")
    context = {"latest_match_day_list": latest_match_day_list, "players_list": players_list}
    return render(request, "stat_track/home.html", context)

def moderator_panel(request):
    return HttpResponse("Moderator Panel")

def player_stats(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render(request, "stat_track/player.html", {"player": player})

def matchday(request, matchday_id):
    matchday = get_object_or_404(MatchDay, pk=matchday_id)
    matches_in_matchday_list = Match.objects.filter(matchday=matchday_id)
    context = {"matches_in_matchday_list": matches_in_matchday_list, "matchday": matchday}
    return render(request, "stat_track/matchday.html", context)

def match_creator_matchday(request):
    if request.method == "POST":
        if "saveMatch" in request.POST:
            selected_players = request.POST.getlist("selected_players")
            request.session['selected_players'] = selected_players

            form = MatchDayForm(request.POST)
            if form.is_valid():
                form.save()

            return redirect('match_creator_matches')


    list_of_players = Player.objects.all().order_by("last_name")
    form = MatchDayForm()
    context = {"list_of_players": list_of_players, "form": form}

    return render(request, "stat_track/match_creator_matchday.html", context)

def match_creator_matches(request):

    selected_players_ids = request.session.get('selected_players', [])
    players_list = Player.objects.filter(id__in=selected_players_ids)
    context = {"players_list": players_list}

    return render(request, "stat_track/match_creator_matches.html", context)