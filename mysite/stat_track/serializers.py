from rest_framework import serializers

from .models import MatchDay, Match, Player, Stat

class MatchDaySerializer(serializers.ModelSerializer):

    matches = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MatchDay
        fields = [
            'date',
            'matches',
            'players',
        ]

    def get_matches(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, MatchDay):
            return None
        

class MatchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Match
        fields = [
            'matchday',
            'team_home',
            'team_away',
            'home_goals',
            'away_goals',
            'winner_team'
        ]

class PlayerSerializer(serializers.ModelSerializer):
    matches_played = serializers.SerializerMethodField(read_only=True)
    goals = serializers.SerializerMethodField(read_only=True)
    points = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Player
        fields = [
            'id',
            'first_name',
            'last_name',
            'matches_played',
            'points',
            'goals',
        ]

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