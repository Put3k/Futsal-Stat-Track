from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

class Player(models.Model):

    def get_matches_played(self):        #get all matches that certain player played in
        return self.match_set.all()

    def __str__(self):
        return self.nickname

    def get_stats(self):
        return Stats.objects.filter(player=self)

    name = models.CharField(max_length=16)
    nickname = models.CharField(max_length=20)

class Match(models.Model):
    date = models.DateTimeField("Date of match")
    players = models.ManyToManyField(Player, blank=True, default="")

    def __str__(self):
        return f"Matchday {self.date.strftime('%d.%m.%Y')}"

class Stats(models.Model):

    TEAM_CHOICES = (
        ("Blue", 'Team Blue'),
        ("Orange", 'Team Orange'),
        ("Colors", 'Team Colors'),
    )

    def positive_validator(value):
        if value < 0:
            raise ValidationError('Value of this field can not be negative.')

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(choices=TEAM_CHOICES, max_length=16)
    goals = models.IntegerField(validators=[positive_validator], default=0)
    wins = models.IntegerField(validators=[positive_validator], default=0)
    loses = models.IntegerField(validators=[positive_validator], default=0)
    draws = models.IntegerField(validators=[positive_validator], default=0)

    def __str__(self):
        return f"ID: {self.id} - {self.player.name} {self.player.nickname} - {self.match}"

    class Meta:
        verbose_name_plural = "Statistics"