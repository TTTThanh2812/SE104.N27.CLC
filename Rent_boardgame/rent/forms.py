from django import forms
from .models import RentBoardgame

class RentBoardgameForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = RentBoardgame
        fields = ['start_date', 'end_date', 'boardgame_numbers']