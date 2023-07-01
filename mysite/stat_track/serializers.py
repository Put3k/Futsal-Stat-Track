from rest_framework import serializers, status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.http import JsonResponse

from .models import MatchDay, MatchDayTicket, Match, Player, Stat


class MatchDaySerializer(serializers.ModelSerializer):

    # Validate if teams field exists in POST data to avoid creating Matchdays with no Players
    def validate(self, data):
        if not "teams" in self.initial_data:
            raise serializers.ValidationError({"teams": "This field is required"})

        if not any(team in self.initial_data['teams'] for team in ['blue', 'orange', 'colors']):
            raise serializers.ValidationError({"teams": "Teams are mandatory"})

        return data


    #Serializer Fields
    matches = serializers.SerializerMethodField()
    teams = serializers.SerializerMethodField()

    class Meta:
        model = MatchDay
        fields = [
            'id',
            'date',
            'matches',
            'teams',
        ]


    #Returns match counter
    def get_matches(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, MatchDay):
            return None
        return obj.match_counter

    #Return teams with list of players ids
    def get_teams(self, obj):
        tickets_dict = MatchDayTicket.objects.filter(matchday=obj).values('player_id', 'team')

        teams_dict = {
            "blue":[],
            "orange":[],
            "colors":[],
        }

        for ticket in tickets_dict:
            if ticket.get('team') == "blue":
                del ticket['team']
                teams_dict["blue"].append(ticket)

            if ticket.get('team') == "orange":
                del ticket['team']
                teams_dict["orange"].append(ticket)

            if ticket.get('team') == "colors":
                del ticket['team']
                teams_dict["colors"].append(ticket)
        return teams_dict


    def create(self, validated_data):
        teams_data = self.initial_data.get('teams')

        matchday = MatchDay.objects.create(**validated_data)

        for team, players in teams_data.items():
            for player_data in players:
                player = Player.objects.get(id=player_data['id'])
                MatchDayTicket.objects.create(matchday=matchday, player=player, team=team)
        return matchday


class MatchSerializer(serializers.ModelSerializer):
    
    #Serializer fields
    goal_scorers = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = [
            'id',
            'matchday',
            'team_home',
            'team_away',
            'home_goals',
            'away_goals',
            'winner_team',
            'goal_scorers'
        ]

    def get_goal_scorers(self, obj):
        team_home = obj.team_home
        team_away = obj.team_away
        matchday = obj.matchday

        team_home_players = MatchDayTicket.objects.filter(matchday=matchday, team=team_home).values('player_id')
        team_away_players = MatchDayTicket.objects.filter(matchday=matchday, team=team_away).values('player_id')

        goal_scorers = {team_home:[], team_away:[]}

        for player in team_home_players:
            player_id = player['player_id']
            player_goals = Stat.objects.filter(player=player_id, match=obj).values('goals').first()
            if player_goals is None or player_goals['goals'] == 0:
                continue
            player_dict = {**player, **player_goals}
            goal_scorers[team_home].append(player_dict)


        for player in team_away_players:
            player_id = player['player_id']
            player_goals = Stat.objects.filter(player=player_id, match=obj).values('goals').first()
            if player_goals is None or player_goals['goals'] == 0:
                continue
            player_dict = {**player, **player_goals}
            goal_scorers[team_away].append(player_dict)

        return goal_scorers
            


class PlayerSerializer(serializers.ModelSerializer):
    matches_played = serializers.SerializerMethodField(read_only=True)
    goals = serializers.SerializerMethodField(read_only=True)
    points = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='player-detail',
        lookup_field='pk'
        )
    class Meta:
        model = Player
        fields = [
            'pk',
            'url',
            'edit_url',
            'first_name',
            'last_name',
            'matches_played',
            'points',
            'goals',
        ]

    def get_edit_url(self, obj):
        request = self.context.get('request')

        if request is None:
            return None
        return reverse("player-edit", kwargs={"pk":obj.pk}, request=request)

    def get_matches_played(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Player):
            return None
        return obj.get_player_matches_played

    def get_points(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Player):
            return None
        return obj.get_total_points
    
    def get_goals(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Player):
            return None
        return obj.get_player_goals