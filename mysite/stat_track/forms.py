from django import forms
from django.forms import ModelForm
from .models import MatchDay, MatchDayTicket, Match, Player

class DateInput(forms.DateInput):
    input_type = 'date'

class MatchDayForm(forms.ModelForm):
    class Meta:
        model = MatchDay
        fields = ['date']
        widgets = {
            'date': DateInput()
        }

class MatchCreator(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['team_home', 'team_away', 'home_goals', 'away_goals']

        widgets = {
            'team_home': forms.Select(attrs={'class':'form-control bg-dark text-white w-75'}),
            'team_away': forms.Select(attrs={'class':'form-control bg-dark text-white w-75'}),
            'home_goals': forms.NumberInput(attrs={'class':'form-control bg-dark text-white w-25'}),
            'away_goals': forms.NumberInput(attrs={'class':'form-control bg-dark text-white w-25'})
        }