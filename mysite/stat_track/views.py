from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    latest_match_list

def moderator_panel(request):
    return HttpResponse("Moderator Panel")

def player_stats(request, player_id):
    response = "You're looking at the Stats of Player %s."
    return HttpResponse(response % player_id)

def match_stats(request, match_id):
    return HttpResponse("You're looking at the stats of Match %s." % match_id)