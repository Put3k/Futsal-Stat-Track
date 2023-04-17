from django.db import models
from datetime import datetime

class Player(models.Model):

    def get_matches_played(self):        #get all matches that certain player played in
        return self.match_set.all()

    def __str__(self):
        return self.nickname

    name = models.CharField(max_length=16)
    nickname = models.CharField(max_length=20)

class Match(models.Model):
    date = models.DateTimeField("Date of match")
    players = models.ManyToManyField(Player, blank=True, default="")

    def __str__(self):
        return f"Matchday {self.date.strftime('%d.%m.%Y')}"