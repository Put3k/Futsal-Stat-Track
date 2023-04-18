from .models import Stats

class StatsForm(forms.ModelForm):
    class Meta:
        model = Stats
        fields = '__all__'
        widgets = {
            'goals': forms.NumberInput(attrs={'min': '0', 'step': '1'}),
            'wins': forms.NumberInput(attrs={'min': '0', 'step': '1'}),
            'loses': forms.NumberInput(attrs={'min': '0', 'step': '1'}),
            'draws': forms.NumberInput(attrs={'min': '0', 'step': '1'}),
        }
