from django.contrib import admin
from django import forms
from .models import Match, MatchDay, MatchDayTicket, Player, Stat

class MatchDayAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')
    readonly_fields = ('match_counter', )

class MatchAdmin(admin.ModelAdmin):
    readonly_fields = ('match_in_matchday',)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'get_player_matches_played', 'get_player_goals', 'get_player_wins', 'get_player_loses', 'get_player_draws')

admin.site.register(MatchDay, MatchDayAdmin)
admin.site.register(MatchDayTicket)
admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Stat)
