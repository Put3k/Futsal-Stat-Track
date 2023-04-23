from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from datetime import datetime

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
            

class MatchDay(models.Model):

    date = models.DateTimeField("Date of match")
    match_counter = models.PositiveIntegerField(default=0, )

    def __str__(self):
        return f"Matchday {self.date.strftime('%d.%m.%Y')}"

class Match(models.Model):

    TEAM_CHOICES = (
        ("Blue", "Team Blue"),
        ("Orange", "Team Orange"),
        ("Colors", "Team Colors")
    )

    matchday = models.ForeignKey(MatchDay, on_delete=models.CASCADE, default=None)
    team_home = models.CharField(choices=TEAM_CHOICES, max_length=20, default="Blue")
    team_away = models.CharField(choices=TEAM_CHOICES, max_length=20, default="Orange")
    home_goals = models.IntegerField()
    away_goals = models.IntegerField()
    match_in_matchday = models.IntegerField(default = 0)

    @property
    def score(self):
        return f"{self.home_goals} - {self.away_goals}"

    @property
    def result(self):                   #returns 1 for home, 2 for away, 0 for draw
        if self.home_goals > self.away_goals:
            return 1
        elif self.home_goals < self.away_goals:
            return 2
        else:
            return 0

    def clean(self):
        #check if team_home and team_away are different

        if self.team_home == self.team_away:
            raise ValidationError("Home team and Away team cannot be the same.")

        if self.home_goals < 0 or self.away_goals < 0:
            raise ValidationError("Goals scored cannot be negative.")

    def __str__(self):
        return f"{self.match_in_matchday}-{self.matchday.date.strftime('%d-%m-%Y')}-{self.team_home}-{self.team_away}"

class Stats(models.Model):

    TEAM_CHOICES = (
        ("Blue", 'Team Blue'),
        ("Orange", 'Team Orange'),
        ("Colors", 'Team Colors'),
    )

    def positive_validator(value):
        """
        Checks if value passed to goals is positive.
        """
        if value < 0:
            raise ValidationError('Value of this field can not be negative.')

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(choices=TEAM_CHOICES, max_length=16)
    goals = models.IntegerField(validators=[positive_validator], default=0)

    def __str__(self):
        return f"ID: {self.id} - {self.match}  - {self.player.first_name} {self.player.last_name}"

@receiver(post_save, sender=Match)
def increment_match_counter(sender, instance, created, **kwargs):
    if created:
        matchday = instance.matchday
        if matchday:
            matchday.match_counter += 1
            matchday.save()
        
        instance.match_in_matchday = matchday.match_counter
        instance.save()

@receiver(post_delete, sender=Match)
def decrement_match_counter(sender, instance, **kwargs):
    matchday = instance.matchday
    if matchday:
        matchday.match_counter -= 1
        matchday.save()