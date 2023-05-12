from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.urls import reverse
from .models import MatchDay, MatchDayTicket, Match, Player, Stat
from .forms import MatchDayForm, MatchCreator, StatForm, PlayerForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction

def home(request):
    latest_match_day_list = MatchDay.objects.order_by("-date")[:5]
    players_list = Player.objects.all().order_by('last_name')

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

    def create_matchday_tickets(list_of_players, matchday, team):
        """Create MatchDayTicket to assign players to teams in certain matchday."""

        for player_id in list_of_players:
            player = Player.objects.filter(pk=player_id).get()
            ticket = MatchDayTicket(matchday=matchday, player=player, team=team)
            ticket.save()

    if request.method == "POST":
        if "saveMatch" in request.POST:

            #Get players sorted by teams.
            team_blue = request.POST.getlist("team_blue")
            team_orange = request.POST.getlist("team_orange")
            team_colors = request.POST.getlist("team_colors")

            #Save MatchDay form and access instance of it.
            form = MatchDayForm(request.POST)
            if form.is_valid():
                matchday = form.save()

            create_matchday_tickets(team_blue, matchday, "blue")
            create_matchday_tickets(team_orange, matchday, "orange")
            create_matchday_tickets(team_colors, matchday, "colors")

            return redirect(f"/matchday/{matchday.id}/edit")

    list_of_players = Player.objects.all().order_by("last_name")
    form = MatchDayForm()
    player_form = PlayerForm()
    
    context = {
        "list_of_players": list_of_players,
        "form": form,
        "player_form":player_form
    }

    return render(request, "stat_track/create_matchday.html", context)

@transaction.atomic
def edit_matchday(request, matchday_id):

    #get matchday
    matchday = get_object_or_404(MatchDay, pk=matchday_id)
    errors = []
    success = None

    if "addMatch" in request.POST:
        form = MatchCreator(request.POST)
        stat_list = []
        stat_counter = 0

        if form.is_valid():
            match = form.save(commit=False)
            match.matchday = matchday

            #Validate sum of goals scored by players
            home_team = match.team_home
            home_sum_of_goals_scored = 0

            away_team = match.team_away
            away_sum_of_goals_scored = 0

            with transaction.atomic():
                match.full_clean()  # Validate match data
                match.save()

                for key, value in request.POST.items():
                    if key.isdigit():
                        stat_counter += 1
                        player = Player.objects.filter(pk=key).first()
                        goals = value
                        stat = Stat(player=player, match=match, goals=goals)

                        try:
                            stat.full_clean()  # Validate stat data
                            stat_list.append(stat)
                        except ValidationError as e:
                            raise

                if len(stat_list) == stat_counter:
                    for stat in stat_list:
                        stat.save()
                    success = 'Match has been added successfully.'
                else:
                    error = 'Error occurred when adding player statistics.'
                    errors.append(error)

        else:
            error = 'Match data is not valid.'
            errors.append(error)

    elif "addPlayer" in request.POST:
        player_form = PlayerForm(request.POST)
        
        if player_form.is_valid():
            player = player_form.save()
            success = f'Player {player} has been added successfully'

            return redirect ('create_matchday')
        else:
            player_form = PlayerForm()

    #get match list for this matchday
    match_list = Match.objects.filter(matchday=matchday)

    #get matchday tickets
    ticket_list = MatchDayTicket.objects.filter(matchday=matchday)

    form = MatchCreator()

    context = {
        "match_list":match_list,
        "matchday":matchday,
        "ticket_list":ticket_list,
        "form":form,
        'errors': errors,
        'success': success
        }

    return render(request, "stat_track/edit_matchday.html", context)

def delete_match(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    matchday_id = match.matchday.id
    match.delete()
    return redirect(f'/matchday/{matchday_id}/edit')


# AJAX
def load_players(request):
    matchday_id = request.GET.get('matchday_id')
    matchday = MatchDay.objects.get(pk=matchday_id)

    team = request.GET.get('team')

    home_data = None
    away_data = None

    data = {}

    if team == "home":

        team_color = request.GET.get('team_home')
        players_home_id_list = MatchDayTicket.objects.filter(matchday=matchday, team=team_color).values_list("player", flat=True)
        players_home = Player.objects.filter(pk__in=players_home_id_list)
        context_home = {"players_home":players_home}

        template_home = "stat_track/players_home_dropdown_list_options.html"
        return render(request, template_home, context_home)
        # data["home_data"] = home_data

    if team == "away":

        team_color = request.GET.get('team_away')
        players_away_id_list = MatchDayTicket.objects.filter(matchday=matchday, team=team_color).values_list("player", flat=True)
        players_away = Player.objects.filter(pk__in=players_away_id_list)
        context_away = {"players_away":players_away}
        template_away = "stat_track/players_away_dropdown_list_options.html"

        return render(request, template_away, context_away)