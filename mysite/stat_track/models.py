from django.db import models, transaction
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from datetime import datetime

TEAM_CHOICES = (
    ("blue", "blue"),
    ("orange", "orange"),
    ("colors", "colors")
)

class Player(models.Model):

    first_name = models.CharField(max_length = 16)
    last_name = models.CharField(max_length = 16)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if Player.objects.filter(first_name=self.first_name, last_name=self.last_name).exists():
            player_id = Player.objects.get(first_name=self.first_name, last_name=self.last_name).id
            raise ValidationError(f"This Player already exists at ID: {player_id}")
        super(Player, self).save(*args, **kwargs)

    def get_player_matches_played(self):
        matches_played = Stat.objects.filter(player=self).count()
        return matches_played

    def get_player_goals(self):
        goals_queryset = Stat.objects.filter(player=self).values_list('goals')
        total_goals = goals_queryset.aggregate(Sum('goals'))['goals__sum']
        if total_goals:
            return total_goals
        else:
            return 0

    def get_player_wins(self):
        stats = Stat.objects.filter(player=self)
        wins = 0
        for stat in stats:
            if stat.win == True:
                wins += 1
        return wins
    
    def get_player_loses(self):
        stats = Stat.objects.filter(player=self)
        loses = 0
        for stat in stats:
            if stat.win == False:
                loses += 1
        return loses

    def get_player_draws(self):
        stats = Stat.objects.filter(player=self)
        draws = 0
        for stat in stats:
            if stat.win == "Draw":
                draws += 1
        return draws

    get_player_matches_played.short_description = 'Matches'
    get_player_goals.short_description = 'Goals'
    get_player_wins.short_description = 'Wins'
    get_player_loses.short_description = 'Loses'
    get_player_draws.short_description = 'Draws'

class MatchDay(models.Model):

    date = models.DateTimeField("Date of match")
    match_counter = models.PositiveIntegerField(default=0, )

    def __str__(self):
        return f"Matchday {self.date.strftime('%d-%m-%Y')}"

class MatchDayTicket(models.Model):
    #Model to store data of players assigned to team in matchday

    matchday = models.ForeignKey(MatchDay, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.CharField(choices=TEAM_CHOICES, max_length=16)

    def __str__(self):
        return f"Ticket-{self.matchday.date.strftime('%d-%m-%Y')}-{self.player.id}-{self.id}"

class Match(models.Model):

    matchday = models.ForeignKey(MatchDay, on_delete=models.CASCADE, default=None)
    team_home = models.CharField(choices=TEAM_CHOICES, max_length=20)
    team_away = models.CharField(choices=TEAM_CHOICES, max_length=20)
    home_goals = models.IntegerField(default=0)
    away_goals = models.IntegerField(default=0)
    match_in_matchday = models.IntegerField(default = 0)

    @property
    def score(self):
        return f"{self.home_goals} - {self.away_goals}"

    @property
    def result(self):   
        """returns 1 for home, 2 for away, 0 for draw"""
        if self.home_goals > self.away_goals:
            return 1
        elif self.home_goals < self.away_goals:
            return 2
        else:
            return 0

    @property
    def winner_team(self):
        """returns color of winner team"""
        if self.result == 1:
            return self.team_home
        elif self.result == 2:
            return self.team_away
        else:
            return None

    @property
    def print_match(self):
        return f"{self.team_home.capitalize()} {self.home_goals} - {self.away_goals} {self.team_away.capitalize()}"

    def clean(self):
        """check if team_home and team_away are different"""

        if self.team_home == self.team_away:
            raise ValidationError("Home team and Away team cannot be the same.")

        if self.home_goals < 0 or self.away_goals < 0:
            raise ValidationError("Goals scored cannot be negative.")

    def __str__(self):
        return f"{self.match_in_matchday}-{self.matchday.date.strftime('%d-%m-%Y')}-{self.team_home}-{self.team_away}"

class Stat(models.Model):

    def positive_validator(value):
        """
        Checks if value passed to goals is positive.
        """
        if value < 0:
            raise ValidationError('Value of this field can not be negative.')

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    goals = models.IntegerField(validators=[positive_validator], default=0)

    def __str__(self):
        return f"ID: {self.id} - {self.match}  - {self.player.first_name} {self.player.last_name}"

    @property
    def get_team(self):
        "Get player team"
        matchday = self.match.matchday

        team = MatchDayTicket.objects.filter(matchday=matchday, player=self.player)['team']
        return team

    @property
    def win(self):
        """Result of match for certain Player"""
        match_winner_team = self.match.winner_team
        if match_winner_team == self.get_team:
            return True
        elif match_winner_team == None:
            return "Draw"
        else:
            return False

    #Validation Functions
    @property
    def player_is_valid(self):
        """Check if Player already exists in match."""

        players = Stat.objects.filter(match=self.match).values_list('player', flat=True)
        if self.player.id in players:
            return False
        else:
            return True

    @property
    def goals_is_valid(self):
        """Chceck if goals scored by player and other teammates sum up to goals declared in Match."""

        if self.get_team == self.match.team_home:
            goals_scored_by_team = self.match.home_goals
        else:
            goals_scored_by_team = self.match.away_goals

        goals_queryset = Stat.objects.filter(match=self.match, team=self.team).values('goals')
        goals_scored_by_teammates = goals_queryset.aggregate(Sum('goals'))['goals__sum']
        if goals_scored_by_teammates == None:
            goals_scored_by_teammates = 0

        if self.goals > goals_scored_by_team - goals_scored_by_teammates:
            return False
        else:
            return True

    @property
    def team_is_valid(self):
        """Check if team assigned to player in stat appears in match."""

        if self.get_team != self.match.team_home and self.get_team != self.match.team_away:
            return False
        else:
            return True

    def clean(self):
        #Player validation
        if not self.player_is_valid:
            raise ValidationError(f'Stat for {self.player} in this match already exists.')

        #Goals validation
        if not self.goals_is_valid:
            raise ValidationError('Sum of the goals of the individual players is greater than the declared match goals.')

        #Team exists in match validation
        if not self.team_is_valid:
            raise ValidationError(f'Team {self.team} does not appear in this match.')


@receiver(post_save, sender=Match)
def increment_match_counter(sender, instance, created, **kwargs):
    """
    Increment match counter in Matchday after creation of Match and set its number.
    """
    if created:
        matchday = instance.matchday
        if matchday:
            matchday.match_counter += 1
            matchday.save()
        
        instance.match_in_matchday = matchday.match_counter
        instance.save()

@receiver(post_delete, sender=Match)
def decrement_match_counter(sender, instance, **kwargs):
    """
    Decrement match counter in Matchday after deletion of Match.
    """
    matchday = instance.matchday
    match_in_matchday = instance.match_in_matchday
    if matchday:
        matchday.match_counter -= 1
        matchday.save()

    with transaction.atomic():
        # Get all Match records in certain MatchDay, which match_in_matchday is greater than deleted value.
        matches_to_decrement = Match.objects.filter(matchday=matchday, match_in_matchday__gt=match_in_matchday)

        # Decrement match_in_matchday in all found records.
        matches_to_decrement.update(match_in_matchday=models.F('match_in_matchday') - 1)