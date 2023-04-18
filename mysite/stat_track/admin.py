from django.contrib import admin
from django import forms
from .models import Match, Player, Stats

class StatsInline(admin.TabularInline):
    model = Stats
    extra = 0

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'name', 'matches_played_list')
    inlines = [StatsInline,]

    def matches_played_list(self, obj):
        matches = obj.get_matches_played()
        return '. '.join(str(match) for match in matches)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        #get player from database
        player = Player.objects.get(pk=object_id)

        #create context
        context = dict(
            self.admin_site.each_context(request),
            player=player,
        )

        return super().change_view(request, object_id, form_url, extra_context=context)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'date')

class StatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'player')

    def save_model(self, request, obj, form, change):
        #Check if Stats for this player in this day already exists.
        try:
            stats = Stats.objects.get(player=obj.player, match=obj.match)
            self.message_user(request, "Stats for this player in this day already exists.", level='error')
        except Stats.DoesNotExist:
            obj.save()

admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Stats, StatsAdmin)
