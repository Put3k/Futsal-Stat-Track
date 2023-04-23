from django.contrib import admin
from django import forms
from .models import Match, MatchDay, Player, Stats

class MatchDayAdmin(admin.ModelAdmin):
    readonly_fields = ('match_counter', )

class MatchAdmin(admin.ModelAdmin):
    readonly_fields = ('match_in_matchday',)

admin.site.register(MatchDay, MatchDayAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Player)
admin.site.register(Stats)
