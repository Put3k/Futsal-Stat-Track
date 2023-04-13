from django.contrib import admin
from django import forms
from .models import Match, Player

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'name', 'matches_played_list')

    def matches_played_list(self, obj):
        matches = obj.get_matches_played()
        return ', '.join(str(match) for match in matches)

admin.site.register(Player, PlayerAdmin)
admin.site.register(Match)
