from django import forms
from django.forms import ModelForm
from .models import MatchDay

class DateInput(forms.DateInput):
    input_type = 'date'

class MatchDayForm(forms.ModelForm):
    class Meta:
        model = MatchDay
        fields = ['date']
        widgets = {
            'date': DateInput()
        }