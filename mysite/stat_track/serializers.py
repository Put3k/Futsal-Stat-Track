from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import MatchDay, MatchDayTicket, Match, Player, Stat

class MatchDaySerializer(serializers.ModelSerializer):

    matches = serializers.SerializerMethodField(read_only=True)
    players = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MatchDay
        fields = [
            'id',
            'date',
            'matches',
            'players',
        ]

    def get_matches(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, MatchDay):
            return None

        return obj.match_counter
        

    def get_players(self, obj):
        players_list = MatchDayTicket.objects.filter(matchday=obj).values('player')
        return players_list
        

class MatchSerializer(serializers.ModelSerializer):
    
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
        ]

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