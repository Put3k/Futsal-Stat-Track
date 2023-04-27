from django import forms
from django.forms import ModelForm, DateInput, DateField
from .models import MatchDay, Match, Player, Stat


#Create match creator form
class DateInput(forms.DateInput):
    input_type= 'date'

class MatchCreator(forms.Form):
    date = forms.DateField(widget=DateInput)
    players = forms.ModelMultipleChoiceField(queryset=Player.objects.all())